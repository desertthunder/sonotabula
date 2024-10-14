"""Model serializers."""

import typing

from django.db import models
from pydantic import BaseModel

from api.models import Playlist, Track, TrackFeatures


class PlaylistModelSerializer(BaseModel):
    """Playlist model serializer."""

    id: str
    name: str
    spotify_url: str
    is_synced: bool | None = False
    is_analyzed: bool | None = False
    description: str | None = None
    owner_id: str | None = None
    version: str | None = None
    image_url: str | None = None
    public: bool | None = None
    shared: bool | None = None

    @classmethod
    def get(
        cls: type["PlaylistModelSerializer"], model: Playlist
    ) -> "PlaylistModelSerializer":
        """Create a model serializer from a model."""
        return cls(
            id=str(model.id),
            name=model.name,
            spotify_url=model.spotify_url,
            is_synced=model.is_synced,
            is_analyzed=model.is_analyzed,
            description=model.description,
            owner_id=model.owner_id,
            version=model.version,
            image_url=model.image_url,
            public=model.public,
            shared=model.shared,
        )

    @classmethod
    def list(
        cls: type["PlaylistModelSerializer"],
        models: models.QuerySet["Playlist"],
    ) -> typing.Iterable["PlaylistModelSerializer"]:
        """Create a list of model serializers from a list of models."""
        for model in models:
            yield cls.get(model)


class TrackFeaturesModelSerializer(BaseModel):
    """Track Features model serializer."""

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

    @classmethod
    def get(
        cls: type["TrackFeaturesModelSerializer"], model: TrackFeatures
    ) -> "TrackFeaturesModelSerializer":
        """Create a model serializer from a model."""
        return cls(
            id=str(model.id),
            danceability=model.danceability,
            energy=model.energy,
            key=model.key,
            loudness=model.loudness,
            mode=model.mode,
            speechiness=model.speechiness,
            acousticness=model.acousticness,
            instrumentalness=model.instrumentalness,
            liveness=model.liveness,
            valence=model.valence,
            tempo=model.tempo,
            duration_ms=model.duration_ms,
            time_signature=model.time_signature,
        )


class TrackModelSerializer(BaseModel):
    """Browser Playlist Track model serializer."""

    id: str
    album_id: str
    name: str
    spotify_id: str
    duration: int
    spotify_url: str
    features: TrackFeaturesModelSerializer | None = None
    album_name: str | None = None
    album_art: str | None = None

    @classmethod
    def get(cls: type["TrackModelSerializer"], model: Track) -> "TrackModelSerializer":
        """Create a model serializer from a model."""
        album_name = None
        features = None
        album_art = None

        if hasattr(model, "album") and model.album is not None:
            album_name = model.album.name
            album_art = model.album.image_url

        if hasattr(model, "features") and model.features is not None:
            features = TrackFeaturesModelSerializer.get(model.features)

        return cls(
            id=str(model.id),
            name=model.name,
            spotify_url=model.spotify_url,
            duration=model.duration,
            spotify_id=model.spotify_id,
            album_id=str(model.album_id),
            album_art=album_art,
            features=features,
            album_name=album_name,
        )

    @classmethod
    def list(
        cls: type["TrackModelSerializer"],
        models: models.QuerySet,
    ) -> typing.Iterable["TrackModelSerializer"]:
        """Create a list of model serializers from a list of models."""
        for model in models:
            yield cls.get(model)
