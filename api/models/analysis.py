"""Analysis models."""

import typing
import uuid

import pandas as pd
from django.db import models
from pydantic import BaseModel

from api.models.music import TimestampedModel
from api.models.playlist import Playlist
from api.models.track import Track
from api.models.users import AppUser


class SyncAnalysis(BaseModel):
    """Track features for analysis."""

    id: str
    danceability: float
    energy: float
    key: int
    loudness: float
    mode: int
    speechiness: float
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float
    tempo: float
    duration_ms: int
    time_signature: int


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
        self, playlist_pk: str, user_pk: int, items: typing.Iterable[dict]
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
            data = SyncAnalysis(**item)
            feature_data = data.model_dump().copy()
            spotify_id = feature_data.pop("id")

            track = playlist.tracks.get(spotify_id=spotify_id)

            TrackFeatures.objects.create(**feature_data, track_id=track.pk)

            tracks.append(track)

        analysis.tracks.set(tracks)
        playlist.is_analyzed = True

        analysis.save()
        playlist.save()

        analysis.refresh_from_db()

        return analysis.pk

    def computation(self, playlist_pk: uuid.UUID) -> pd.DataFrame:
        """Calculate playlist analysis."""
        playlist_track_pks = (
            Playlist.objects.get(pk=playlist_pk)
            .tracks.all()
            .values_list("pk", flat=True)
        )
        features = TrackFeatures.objects.filter(track__in=playlist_track_pks).values()

        return pd.DataFrame(features)  # type: ignore


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
    user = models.ForeignKey("api.AppUser", on_delete=models.CASCADE)
    tracks = models.ManyToManyField("api.Track", related_name="analyses")

    objects: models.Manager["Analysis"] = models.Manager()
    sync: AnalysisManager = AnalysisManager()
