"""Analysis models.

(TODO): Reassess need for tracks foreign key in Analysis model.
(TODO): Add album as foreign key to Track model.
"""

import typing
import uuid

import numpy as np
import pandas as pd
from django.db import models
from loguru import logger

from api.models.mixins import TimestampedModel
from api.models.playlist import Playlist
from api.models.track import Track
from api.serializers import validation
from core.models import AppUser


class AnalysisManager(models.Manager["Analysis"]):
    """Manager for analysis models."""

    def pre_analysis(self, playlist_pk: uuid.UUID, user_pk: int) -> list[str]:
        """Analyze a playlist."""
        playlist = Playlist.objects.get(pk=playlist_pk)

        if not playlist.is_synced:
            raise ValueError(
                f"Playlist {str(playlist.pk)} | {playlist.name} is not synced."
            )

        results = playlist.tracks.all().values_list("spotify_id", flat=True)

        return list(results)

    def analyze(
        self, playlist_pk: str | uuid.UUID, user_pk: int, items: typing.Iterable[dict]
    ) -> uuid.UUID:
        """Validate track data."""
        playlist = Playlist.objects.get(pk=playlist_pk)
        user = AppUser.objects.get(pk=user_pk)

        if not playlist.is_synced:
            raise ValueError(
                f"Playlist {str(playlist.pk)} | {playlist.name} is not synced."
            )

        analysis, _ = self.get_or_create(
            version=playlist.version, playlist_id=playlist.pk, user=user
        )  # type: ignore

        tracks = []

        for item in items:
            data = validation.SyncAnalysis(**item)
            feature_data = data.model_dump().copy()
            spotify_id = feature_data.pop("id")

            track = playlist.tracks.get(spotify_id=spotify_id)

            _ = TrackFeatures.objects.get_or_create(**feature_data, track_id=track.pk)

            tracks.append(track)

        analysis.tracks.set(tracks)
        playlist.is_analyzed = True

        analysis.save()
        playlist.save()

        analysis.refresh_from_db()

        return analysis.pk

    def build_dataset(self, analysis_pk: uuid.UUID) -> pd.DataFrame:
        """Calculate playlist analysis."""
        features = (
            TrackFeatures.objects.filter(track__analyses__id=analysis_pk).all().values()
        )

        df = pd.DataFrame(features)  # type: ignore

        return df

    def compute(self, analysis_pk: uuid.UUID) -> dict:
        """Compute playlist analysis.

        1. Build the dataset
        2. Calculate averages, superlatives, and counts.
        3. Return the computed data.
        """
        data = self.build_dataset(analysis_pk)

        logger.debug(f"Data: {data.head()}")

        computation_fields = [
            "danceability",
            "energy",
            "key",
            "loudness",
            "mode",
            "speechiness",
            "acousticness",
            "instrumentalness",
            "liveness",
            "valence",
            "tempo",
            "duration_ms",
            "time_signature",
        ]

        counting_fields = ["key", "mode", "time_signature"]

        computed_data: dict[str, dict] = {
            "superlatives": {},
            "averages": {},
            "count": {},
        }

        for field in computation_fields:
            computed_data["averages"][field] = data[field].mean()
            min_value = data[field].min()
            max_value = data[field].max()

            # Serialize numpy float64 to python float
            if isinstance(np.float64, type(min_value)):
                min_value = float(min_value)
            else:
                min_value = int(min_value)

            if isinstance(np.float64, type(max_value)):
                max_value = float(max_value)
            else:
                max_value = int(max_value)

            computed_data["superlatives"][field] = {
                "min": min_value,
                "min_track_id": str(data["track_id"].loc[data[field].idxmin()]),
                "max": max_value,
                "max_track_id": str(data["track_id"].loc[data[field].idxmax()]),
            }

        for field in counting_fields:
            computed_data["count"][field] = data[field].value_counts().to_dict()

        return computed_data

    def set_computation(self, analysis_pk: uuid.UUID, data: dict) -> uuid.UUID:
        """Set computation data.

        Persist the computed data to the database.
        Returns the computation primary key.
        """
        analysis = self.model.objects.get(id=analysis_pk)

        logger.debug(f"Computation Data: {data}")

        computation, _ = Computation.objects.get_or_create(
            analysis_id=analysis.pk,
            playlist_id=analysis.playlist.pk,
            data=data,
        )

        logger.debug(f"Computation: {computation}")

        return computation.pk


class TrackFeatures(TimestampedModel):
    """Track feature record.

    One-to-one relationship with Track model.
    """

    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    track = models.OneToOneField(
        Track, on_delete=models.CASCADE, related_name="features"
    )

    danceability = models.FloatField()
    energy = models.FloatField()
    key = models.IntegerField()
    loudness = models.FloatField()
    mode = models.IntegerField()
    speechiness = models.FloatField()
    acousticness = models.FloatField()
    instrumentalness = models.FloatField()
    liveness = models.FloatField()
    valence = models.FloatField()
    tempo = models.FloatField()
    duration_ms = models.IntegerField()
    time_signature = models.IntegerField()


class Analysis(TimestampedModel):
    """Analysis model.

    Constructed from a single playlist (one-to-one relationship).

    Has many tracks.

    Represents a snapshot of the playlist at a given time,
    with associated tracks.
    """

    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    version = models.CharField(max_length=255, unique=True, null=False)
    playlist = models.OneToOneField(
        Playlist, on_delete=models.CASCADE, related_name="analysis"
    )
    user = models.ForeignKey("core.AppUser", on_delete=models.CASCADE)
    tracks = models.ManyToManyField("api.Track", related_name="analyses")

    objects: models.Manager["Analysis"] = models.Manager()
    sync: AnalysisManager = AnalysisManager()


class Computation(TimestampedModel):
    """Computation model.

    Represents a computed analysis of a playlist.

    Averages, Max, Min of the following:
    - Danceability
    - Energy
    - Loudness
    - Speechiness
    - Acousticness
    - Instrumentalness
    - Liveness
    - Valence
    - Tempo
    - Duration

    Frequency of the following:
    - Key
    - Mode
    - Time Signature
    """

    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    analysis = models.OneToOneField(
        Analysis, on_delete=models.CASCADE, related_name="data"
    )
    playlist = models.ForeignKey(
        Playlist, on_delete=models.CASCADE, related_name="computation"
    )
    data = models.JSONField(
        validators=[validation.ComputationValidator.validate_data], null=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
