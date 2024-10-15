"""Analysis model object validators."""

import pydantic
from django.core.exceptions import ValidationError
from pydantic import BaseModel


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
