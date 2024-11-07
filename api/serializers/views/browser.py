"""Browser view serializers.

GET /api/browser/{model}/
"""

import typing

from django.core.paginator import Paginator
from django.db import models
from pydantic import BaseModel

from api.models import Album, Track


class Pagination(typing.TypedDict):
    """Pagination type."""

    total: int
    per_page: int
    page: int
    num_pages: int


# /browser/albums/
class AlbumArtistSerializer(BaseModel):
    """Simple Artist model serializer."""

    id: str
    name: str
    spotify_id: str


class AlbumModelSerializer(BaseModel):
    """Album model serializer."""

    id: str
    name: str
    artists: list[AlbumArtistSerializer]
    spotify_id: str
    release_year: int
    tracks: list[dict] | None = None
    image_url: str | None = None

    @classmethod
    def get(
        cls: type["AlbumModelSerializer"],
        model: Album,
    ) -> "AlbumModelSerializer":
        """Create a model serializer from a model."""
        return cls(
            id=str(model.id),
            name=model.name,
            artists=[
                AlbumArtistSerializer(
                    id=str(artist.id), name=artist.name, spotify_id=artist.spotify_id
                )
                for artist in model.artists.all()
            ],
            spotify_id=model.spotify_id,
            release_year=model.release_year,
            image_url=model.image_url,
        )


class PaginatedAlbumListSerializer(BaseModel):
    """Paginated Album Serializer."""

    data: list[dict]
    pagination: Pagination

    @classmethod
    def from_paginator(
        cls: type["PaginatedAlbumListSerializer"],
        paginator: Paginator,
        page: int = 1,
    ) -> "PaginatedAlbumListSerializer":
        """Create a model serializer from a paginator."""
        objects = paginator.page(page).object_list

        return cls(
            data=[AlbumModelSerializer.get(record).model_dump() for record in objects],
            pagination={
                "total": paginator.count,
                "per_page": paginator.per_page,
                "page": paginator.page(page).number,
                "num_pages": paginator.num_pages,
            },
        )


# /browser/tracks/
class TrackModelSerializer(BaseModel):
    """Track model serializer."""

    id: str
    name: str
    spotify_id: str
    duration: int
    spotify_url: str
    album_id: str
    is_synced: bool | None = False
    is_analyzed: bool | None = False
    album_name: str | None = None
    album_art: str | None = None

    @classmethod
    def get(cls: type["TrackModelSerializer"], model: Track) -> "TrackModelSerializer":
        """Create a model serializer from a model."""
        album_name = None
        album_art = None

        if hasattr(model, "album") and model.album is not None:
            album_name = model.album.name
            album_art = model.album.image_url

        return cls(
            id=str(model.id),
            name=model.name,
            spotify_url=model.spotify_url,
            duration=model.duration,
            spotify_id=model.spotify_id,
            album_id=str(model.album_id),
            album_name=album_name,
            album_art=album_art,
            is_synced=model.is_synced,
            is_analyzed=model.is_analyzed,
        )

    @classmethod
    def list(
        cls: type["TrackModelSerializer"],
        models: models.QuerySet,
    ) -> typing.Iterable["TrackModelSerializer"]:
        """Create a list of model serializers from a list of models."""
        for model in models:
            yield cls.get(model)


class PaginatedTrackListSerializer(BaseModel):
    """Paginated Track Serializer."""

    data: list[dict]
    pagination: Pagination

    @classmethod
    def from_paginator(
        cls: type["PaginatedTrackListSerializer"],
        paginator: Paginator,
        page: int = 1,
    ) -> "PaginatedTrackListSerializer":
        """Create a model serializer from a paginator."""
        objects = paginator.page(page).object_list

        return cls(
            data=[TrackModelSerializer.get(record).model_dump() for record in objects],
            pagination={
                "total": paginator.count,
                "per_page": paginator.per_page,
                "page": paginator.page(page).number,
                "num_pages": paginator.num_pages,
            },
        )
