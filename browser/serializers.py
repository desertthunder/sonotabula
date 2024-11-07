"""Browser API Response serializers."""

import enum
import typing

from celery import states
from celery.result import AsyncResult
from django.core.paginator import Paginator
from django.db import models
from pydantic import BaseModel

from api.models.album import Album
from api.models.analysis import Computation, TrackFeatures
from api.models.music import Artist
from api.models.playlist import Playlist
from api.models.track import Track

#########################################
# Constants, Mixins, & Base Classes     #
#########################################


class TaskState(enum.StrEnum):
    """Celery task states."""

    PENDING = states.PENDING
    RECEIVED = states.RECEIVED
    STARTED = states.STARTED
    SUCCESS = states.SUCCESS
    FAILURE = states.FAILURE
    REVOKED = states.REVOKED
    REJECTED = states.REJECTED
    RETRY = states.RETRY
    IGNORED = states.IGNORED


class PaginationParams(BaseModel):
    """Pagination parameters."""

    page: int
    page_size: int


class ListResponseMixin:
    """List response method."""

    @classmethod
    def to_response(
        cls: type[typing.Self],
        qs: models.QuerySet,
        params: PaginationParams,
    ) -> dict:
        """Convert data to a response."""
        raise NotImplementedError


class Serializer(BaseModel):
    """Base Serializer class."""

    pass


class Pagination(Serializer):
    """Pagination attributes for list serializers."""

    total: int
    per_page: int
    page: int
    num_pages: int


#########################################
# Playlist Serializer Classes           #
#########################################


class PlaylistBaseSerializer(Serializer):
    """Base serializer for Playlist objects."""

    id: str
    name: str
    spotify_id: str
    num_tracks: int | None = None
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
        cls: type["PlaylistBaseSerializer"], model: Playlist
    ) -> "PlaylistBaseSerializer":
        """Create a model serializer from a model."""
        num_tracks = Playlist.objects.get(id=model.id).tracks.count()

        return cls(
            id=str(model.id),
            name=model.name,
            spotify_id=model.spotify_id,
            is_synced=model.is_synced,
            is_analyzed=model.is_analyzed,
            description=model.description,
            owner_id=model.owner_id,
            version=model.version,
            image_url=model.image_url,
            public=model.public,
            shared=model.shared,
            num_tracks=num_tracks,
        )


class ListPlaylistSerializer(ListResponseMixin, Serializer):
    """Serializer for listing Playlist objects in the browser context."""

    data: list[PlaylistBaseSerializer]
    pagination: Pagination

    @classmethod
    def to_response(
        cls: type["ListPlaylistSerializer"],
        qs: models.QuerySet,
        params: PaginationParams,
    ) -> dict:
        """Convert data to a response."""
        paginator = Paginator(qs.all(), per_page=params.page_size)

        data = []

        for obj in paginator.page(params.page):
            _cls = PlaylistBaseSerializer
            _data = _cls.model_construct()
            _data.id = str(obj.id)
            _data.name = obj.name
            _data.spotify_id = obj.spotify_id
            _data.is_analyzed = obj.is_analyzed
            _data.is_synced = obj.is_synced
            _data.description = obj.description
            _data.owner_id = obj.owner_id
            _data.version = obj.version
            _data.image_url = obj.image_url
            _data.public = obj.public
            _data.shared = obj.shared

            _cls.model_validate(_data)

            data.append(_data)

        pagination = Pagination(
            total=paginator.count,
            per_page=params.page_size,
            page=params.page,
            num_pages=paginator.num_pages,
        )

        return cls(data=data, pagination=pagination).model_dump()


class CreatePlaylistTaskSerializer(Serializer):
    """Serializer for creating PlaylistTask objects in the browser context."""

    pass


class UpdatePlaylistTaskSerializer(Serializer):
    """Serializer for updating PlaylistTask objects in the browser context."""

    pass


#########################################
# Task Result Serializer Classes        #
#########################################


class TaskResultSerializer(Serializer):
    """Serializer for TaskResult objects in the browser context."""

    task_id: str
    status: TaskState

    @classmethod
    def from_result(
        cls: type["TaskResultSerializer"], result: AsyncResult
    ) -> "TaskResultSerializer":
        """Create a TaskResultSerializer from an AsyncResult."""
        return cls(task_id=result.task_id, status=TaskState(result.status))


#########################################
# Album Serializer Classes              #
#########################################


class AlbumArtistSerializer(Serializer):
    """Simple Artist model serializer."""

    id: str
    name: str
    spotify_id: str


class AlbumTrackSerializer(Serializer):
    """Serializes a Track object in the browser context."""

    id: str
    name: str
    spotify_id: str


class AlbumBaseSerializer(Serializer):
    """Serializes an Album objects in the browser context."""

    id: str
    name: str
    artists: list[AlbumArtistSerializer]
    spotify_id: str
    release_year: int
    tracks: list[AlbumTrackSerializer]
    image_url: str | None = None


class ListAlbumSerializer(ListResponseMixin, Serializer):
    """Serializes a collection of filtered Album objects in the browser context."""

    data: list[AlbumBaseSerializer]
    pagination: Pagination

    @classmethod
    def to_response(
        cls: type["ListAlbumSerializer"],
        qs: models.QuerySet,
        params: PaginationParams,
    ) -> dict:
        """Convert data to a response."""
        paginator = Paginator(qs.all(), per_page=params.page_size)

        data = []

        for obj in paginator.page(params.page):
            _cls = AlbumBaseSerializer
            _data = _cls.model_construct()
            _data.id = str(obj.id)
            _data.name = obj.name
            _data.spotify_id = obj.spotify_id
            _data.release_year = obj.release_year
            _data.image_url = obj.image_url
            _data.artists = [
                AlbumArtistSerializer(
                    id=str(artist.id), name=artist.name, spotify_id=artist.spotify_id
                )
                for artist in obj.artists.all()
            ]
            _data.tracks = [
                AlbumTrackSerializer(
                    id=str(track.id),
                    name=track.name,
                    spotify_id=track.spotify_id,
                )
                for track in obj.tracks.all()
            ]
            _cls.model_validate(_data)

            data.append(_data)

        pagination = Pagination(
            total=paginator.count,
            per_page=params.page_size,
            page=params.page,
            num_pages=paginator.num_pages,
        )

        return cls(data=data, pagination=pagination).model_dump()


class RetrieveAlbumSerializer(AlbumBaseSerializer):
    """Serializes an Album object in the browser context."""

    @classmethod
    def get(
        cls: type["RetrieveAlbumSerializer"], model: Album
    ) -> "RetrieveAlbumSerializer":
        """Create a model serializer from a model."""
        album = AlbumBaseSerializer.model_construct()
        album.id = str(model.id)
        album.name = model.name
        album.spotify_id = model.spotify_id
        album.release_year = model.release_year
        album.image_url = model.image_url
        album.artists = [
            AlbumArtistSerializer(
                id=str(artist.id), name=artist.name, spotify_id=artist.spotify_id
            )
            for artist in model.artists.all()
        ]
        album.tracks = [
            AlbumTrackSerializer(
                id=str(track.id),
                name=track.name,
                spotify_id=track.spotify_id,
            )
            for track in model.tracks.all()
        ]

        return cls(**album.model_dump())


#########################################
# Playlist Retrieval Serializer Classes #
#########################################


class PlaylistComputationSerializer(Serializer):
    """Computation model serializer."""

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

        danceability: "PlaylistComputationSerializer.Superlative"
        energy: "PlaylistComputationSerializer.Superlative"
        loudness: "PlaylistComputationSerializer.Superlative"
        speechiness: "PlaylistComputationSerializer.Superlative"
        acousticness: "PlaylistComputationSerializer.Superlative"
        instrumentalness: "PlaylistComputationSerializer.Superlative"
        liveness: "PlaylistComputationSerializer.Superlative"
        valence: "PlaylistComputationSerializer.Superlative"
        tempo: "PlaylistComputationSerializer.Superlative"
        duration_ms: "PlaylistComputationSerializer.Superlative"

    class CountedFields(BaseModel):
        """Counted fields for a playlist."""

        key: dict[int, int]
        mode: dict[int, int]
        time_signature: dict[int, int]

    superlatives: MinMax
    averages: Averages
    count: CountedFields

    @classmethod
    def get(
        cls: type["PlaylistComputationSerializer"], model: Computation
    ) -> "PlaylistComputationSerializer":
        """Create a model serializer from a model."""
        return cls(**model.data)


class PlaylistTrackFeaturesSerializer(Serializer):
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
        cls: type["PlaylistTrackFeaturesSerializer"], model: TrackFeatures
    ) -> "PlaylistTrackFeaturesSerializer":
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


class PlaylistTrackArtistSerializer(Serializer):
    """Track Artist model serializer."""

    id: str
    name: str
    spotify_id: str

    @classmethod
    def get(
        cls: type["PlaylistTrackArtistSerializer"], model: Artist
    ) -> "PlaylistTrackArtistSerializer":
        """Create a model serializer from a model."""
        return cls(
            id=str(model.id),
            name=model.name,
            spotify_id=model.spotify_id,
        )


class PlaylistTrackSerializer(Serializer):
    """Browser Playlist Track model serializer."""

    id: str
    album_id: str
    name: str
    spotify_id: str
    duration: int
    spotify_url: str
    features: PlaylistTrackFeaturesSerializer | None = None
    album_name: str | None = None
    album_art: str | None = None
    artists: list[PlaylistTrackArtistSerializer] | None = None

    @classmethod
    def from_paginator(
        cls: type["PlaylistTrackSerializer"],
        paginator: Paginator,
        page: int = 1,
        playlist: Playlist | None = None,
        computation: Computation | None = None,
    ) -> dict[str, typing.Any]:
        """Create a model serializer from a paginator."""
        objects = paginator.page(page).object_list

        data: dict[str, typing.Any] = {
            "data": {
                "playlist": None,
                "tracks": [cls.get(record).model_dump() for record in objects],
                "computations": None,
            },
            "paginator": {
                "total": paginator.count,
                "per_page": paginator.per_page,
                "page": paginator.page(page).number,
            },
        }

        if playlist is not None:
            data["data"]["playlist"] = PlaylistBaseSerializer.get(playlist).model_dump()

        if computation is not None:
            data["data"]["computations"] = PlaylistComputationSerializer.get(
                computation
            ).model_dump()

        return data

    @classmethod
    def get(
        cls: type["PlaylistTrackSerializer"], model: Track
    ) -> "PlaylistTrackSerializer":
        """Create a model serializer from a model."""
        album_name = None
        features = None
        album_art = None
        artists = None

        if hasattr(model, "album") and model.album is not None:
            album_name = model.album.name
            album_art = model.album.image_url

            if hasattr(model.album, "artists") and model.album.artists is not None:
                artists = [
                    PlaylistTrackArtistSerializer.get(artist)
                    for artist in model.album.artists.all()
                ]

        if hasattr(model, "features") and model.features is not None:
            features = PlaylistTrackFeaturesSerializer.get(model.features)

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
            artists=artists,
        )

    @classmethod
    def list(
        cls: type["PlaylistTrackSerializer"],
        models: models.QuerySet,
    ) -> typing.Iterable["PlaylistTrackSerializer"]:
        """Create a list of model serializers from a list of models."""
        for model in models:
            yield cls.get(model)


class RetrievePlaylistSerializer(Serializer):
    """Expanded Playlist serializer."""

    playlist: PlaylistBaseSerializer
    computations: PlaylistComputationSerializer | None = None
    tracks: list[PlaylistTrackSerializer] | None = None

    @classmethod
    def get(
        cls: type["RetrievePlaylistSerializer"], model: Playlist
    ) -> "RetrievePlaylistSerializer":
        """Create a model serializer from a model."""
        if hasattr(model, "analysis") and model.analysis is not None:
            analysis = model.analysis
            tracks = analysis.tracks.all()

            if hasattr(analysis, "data") and analysis.data is not None:
                computations = analysis.data

            return cls(
                playlist=PlaylistBaseSerializer.get(model),
                computations=PlaylistComputationSerializer.get(computations)
                if computations
                else None,
                tracks=[PlaylistTrackSerializer.get(track) for track in tracks],
            )
        elif hasattr(model, "tracks") and model.tracks is not None:
            return cls(
                playlist=PlaylistBaseSerializer.get(model),
                computations=None,
                tracks=[
                    PlaylistTrackSerializer.get(track) for track in model.tracks.all()
                ],
            )

        return cls(
            playlist=PlaylistBaseSerializer.get(model),
            computations=None,
            tracks=None,
        )

    @classmethod
    def to_response(
        cls: type["RetrievePlaylistSerializer"],
        model: Playlist,
    ) -> dict[str, typing.Any]:
        """Create a model serializer from a model."""
        return {"data": cls.get(model).model_dump()}
