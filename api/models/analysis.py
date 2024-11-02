"""Analysis models.

Contains Django orm models for playlist and album analysis,
as well as persisted computations, based on audio features
provided by the Spotify API.
"""

import typing
import uuid

import pandas as pd
from django.db import models
from loguru import logger

from api.models.album import Album
from api.models.mixins import TimestampedModel
from api.models.playlist import Playlist
from api.models.track import Track
from api.serializers import validation
from core.models import AppUser


class AnalysisManager(models.Manager["Analysis"]):
    """Manager for analysis models."""

    # ALBUM ANALYSIS CREATION
    def prep_album(self, album_pk: uuid.UUID, user_pk: int) -> list[str]:
        """Analyze an album."""
        album = Album.objects.get(pk=album_pk)

        if not album.is_synced:
            raise ValueError(f"Album {str(album.pk)} | {album.name} is not synced.")

        results = album.tracks.all().values_list("spotify_id", flat=True)

        return list(results)

    def analyze_album(
        self, album_pk: str | uuid.UUID, user_pk: int, items: typing.Iterable[dict]
    ) -> uuid.UUID:
        """Validate track data."""
        album = Album.objects.get(pk=album_pk)
        user = AppUser.objects.get(pk=user_pk)

        if not album.is_synced:
            raise ValueError(f"Album {str(album.pk)} | {album.name} is not synced.")

        analysis, _ = self.get_or_create(
            version=f"album:{album.pk}",
            album_id=album.pk,
            user=user,
        )

        tracks = []

        for item in items:
            data = validation.SyncAnalysis(**item)
            feature_data = data.model_dump().copy()
            spotify_id = feature_data.pop("id")

            track = album.tracks.get(spotify_id=spotify_id)

            _ = TrackFeatures.objects.get_or_create(**feature_data, track_id=track.pk)

            tracks.append(track)

        analysis.tracks.set(tracks)
        album.is_analyzed = True

        analysis.save()
        album.save()

        analysis.refresh_from_db()

        return analysis.pk

    # PLAYLIST ANALYSIS CREATION
    def pre_analysis(self, playlist_pk: uuid.UUID, user_pk: int) -> list[str]:
        """Setup playlist analysis.

        Retrieves the list of track Spotify IDs from the playlist record
        to fetch the audio features from the Spotify API.
        """
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
        """Validate track data.

        Builds an analysis record from the playlist and track data provided by
        the Spotify API.

        The playlist from the database is retrieved, then checked for the existence
        of an Analysis object with the same version tag. If the playlist is
        already analyzed, the function returns the primary key of the existing
        Analysis object.
        """
        playlist = Playlist.objects.get(pk=playlist_pk)
        user = AppUser.objects.get(pk=user_pk)

        if not playlist.is_synced:
            raise ValueError(
                f"Playlist {str(playlist.pk)} | {playlist.name} is not synced."
            )

        version_tag = (
            f"version:{playlist.pk}:{playlist.version}"
            if playlist.version
            else f"playlist:{playlist.pk}"
        )

        if playlist.is_analyzed and self.filter(version=version_tag).exists():
            logger.info(f"Playlist {playlist.pk} is already analyzed.")
            logger.debug(f"Version Tag: {version_tag}")
            return self.get(version=version_tag).pk

        analysis, _ = self.update_or_create(
            playlist_id=playlist.pk,
            user=user,
            defaults={
                "version": version_tag,
            },
        )

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

    # COMPUTATION OPERATIONS
    def build_dataset(self, analysis_pk: uuid.UUID) -> pd.DataFrame:
        """Calculate playlist stats."""
        features = (
            TrackFeatures.objects.filter(
                track__analyses__id=analysis_pk,
            )
            .all()
            .values()
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

            computed_data["superlatives"][field] = {
                "min": str(min_value),
                "min_track_id": str(data["track_id"].loc[data[field].idxmin()]),
                "max": str(max_value),
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

        if analysis.playlist is not None:
            computation, _ = Computation.objects.update_or_create(
                analysis_id=analysis.pk,
                playlist_id=analysis.playlist.pk,
                defaults={"data": data},
            )

            logger.debug(f"Computation: {computation}")

            return computation.pk

        if analysis.album is not None:
            computation, _ = Computation.objects.get_or_create(
                analysis_id=analysis.pk,
                album_id=analysis.album.pk,
                data=data,
            )

            logger.debug(f"Computation: {computation}")

            return computation.pk

        raise ValueError("Analysis must have a playlist or album.")


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
        Playlist, on_delete=models.CASCADE, related_name="analysis", null=True
    )
    album = models.OneToOneField(
        Album, on_delete=models.CASCADE, related_name="analysis", null=True
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
        "api.Playlist", on_delete=models.CASCADE, related_name="computation", null=True
    )
    album = models.ForeignKey(
        "api.Album", on_delete=models.CASCADE, related_name="computation", null=True
    )
    data = models.JSONField(
        validators=[validation.ComputationValidator.validate_data], null=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
