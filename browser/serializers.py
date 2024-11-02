"""Browser API Response serializers."""

import enum
import typing

from celery import states
from celery.result import AsyncResult
from django.core.paginator import Paginator
from django.db import models
from pydantic import BaseModel

from api.models.playlist import Playlist


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


# from api.models import Album, Playlist, Track, TrackFeatures, Computation
# from api.models.analysis import Computation
# from api.serializers.validation import ComputationValidator


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


class PlaylistBaseSerializer(Serializer):
    """Base serializer for Playlist objects."""

    id: str
    name: str
    spotify_id: str
    is_synced: bool | None = False
    is_analyzed: bool | None = False
    description: str | None = None
    owner_id: str | None = None
    version: str | None = None
    image_url: str | None = None
    public: bool | None = None
    shared: bool | None = None


class Pagination(Serializer):
    """Pagination attributes for list serializers."""

    total: int
    per_page: int
    page: int
    num_pages: int


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


class RetrievePlaylistSerializer(Serializer):
    """Serializer for retrieving Playlist objects in the browser context."""

    @classmethod
    def to_response_data(
        cls: type["RetrievePlaylistSerializer"], obj: Playlist
    ) -> dict:
        """Convert data to a response."""
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

        return _data.model_dump()


class CreatePlaylistTaskSerializer(Serializer):
    """Serializer for creating PlaylistTask objects in the browser context."""

    pass


class UpdatePlaylistTaskSerializer(Serializer):
    """Serializer for updating PlaylistTask objects in the browser context."""

    pass


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
