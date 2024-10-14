"""Analysis models."""

import typing
import uuid

import pandas as pd
import pydantic
from django.core.exceptions import ValidationError
from django.db import models
from loguru import logger
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
        """Compute playlist analysis."""
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

            computed_data["superlatives"][field] = {
                "min": data[field].min(),
                "min_track_id": str(data["track_id"].loc[data[field].idxmin()]),
                "max": data[field].max(),
                "max_track_id": str(data["track_id"].loc[data[field].idxmax()]),
            }

        for field in counting_fields:
            computed_data["count"][field] = data[field].value_counts().to_dict()

        return computed_data

    def set_computation(self, analysis_pk: uuid.UUID, data: dict) -> uuid.UUID:
        """Set computation data."""
        analysis = Analysis.objects.get(id=analysis_pk)

        computation, _ = Computation.objects.get_or_create(
            analysis_id=analysis.pk, playlist_id=analysis.playlist.pk, data=data
        )

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
    user = models.ForeignKey("api.AppUser", on_delete=models.CASCADE)
    tracks = models.ManyToManyField("api.Track", related_name="analyses")

    objects: models.Manager["Analysis"] = models.Manager()
    sync: AnalysisManager = AnalysisManager()


class Averages(BaseModel):
    """Computed fields for a playlist."""

    danceability: float
    energy: float
    loudness: float
    speechiness: float
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float
    tempo: float
    duration_ms: int | float


class Superlative(BaseModel):
    """Computed fields for a playlist."""

    min: float
    min_track_id: str
    max: float
    max_track_id: str


class MinMax(BaseModel):
    """Computed fields for a playlist."""

    danceability: Superlative
    energy: Superlative
    loudness: Superlative
    speechiness: Superlative
    acousticness: Superlative
    instrumentalness: Superlative
    liveness: Superlative
    valence: Superlative
    tempo: Superlative
    duration_ms: Superlative


class CountedFields(BaseModel):
    """Counted fields for a playlist."""

    key: dict[int, int]
    mode: dict[int, int]
    time_signature: dict[int, int]


class ComputationValidator(BaseModel):
    """Computation data validator."""

    superlatives: MinMax
    averages: Averages
    count: CountedFields

    @classmethod
    def validate_data(cls: type["ComputationValidator"], data: dict) -> None:
        """Validate computation data."""
        try:
            cls(**data)
        except pydantic.ValidationError as e:
            raise ValidationError(e.errors()) from e


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
    data = models.JSONField(validators=[ComputationValidator.validate_data], null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
