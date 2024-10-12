"""Model serializers."""

import typing

from django.db import models
from pydantic import BaseModel

from api.models.playlist import Playlist


class PlaylistModelSerializer(BaseModel):
    """Playlist model serializer."""

    id: str
    name: str
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
        cls: type["PlaylistModelSerializer"], models: models.QuerySet["Playlist"]
    ) -> typing.Iterable["PlaylistModelSerializer"]:
        """Create a list of model serializers from a list of models."""
        for model in models:
            yield cls.get(model)
