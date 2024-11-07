"""Browser ViewSets.

Primary viewsets for feature context collections.
These are audio features stored under a user's
"Library."
"""

import typing
import uuid

from celery import group
from django.core.paginator import Paginator
from django.db import models
from loguru import logger
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from api.models.permissions import SpotifyAuth
from api.models.playlist import Playlist
from browser.filters import AlbumFilterSet, PlaylistFilterSet
from browser.models import Library
from browser.serializers import (
    ListAlbumSerializer,
    ListPlaylistSerializer,
    PaginationParams,
    RetrieveAlbumSerializer,
    RetrievePlaylistSerializer,
    TaskResultSerializer,
)
from browser.tasks import (
    analyze_playlist,
    sync_and_analyze_playlist,
    sync_playlist,
)
from core.filters import FilterSet


class LibraryRelationMixin(typing.Protocol):
    """Relation property protocol for library mixin."""

    @property
    def relation(self) -> str:
        """Get the relation name."""
        ...


class GetUserMixin:
    """Get user mixin."""

    pass


class GetLibraryMixin:
    """Get library mixin."""

    relation: str

    def get_library(self: LibraryRelationMixin, request: Request) -> Library:
        """Get library."""
        logger.debug(f"Getting library for user {request.user.id}")
        return Library.objects.prefetch_related(
            self.relation,
        ).get(
            user_id=request.user.id,
        )


class PaginationParamsMixin:
    """Pagination parameters mixin."""

    def get_params(self: typing.Self, request: Request) -> PaginationParams:
        """Get pagination parameters."""
        page = request.query_params.get("page", 1)
        page_size = request.query_params.get("page_size", 10)

        return PaginationParams(page=int(page), page_size=int(page_size))


class BaseBrowserViewSet(
    ViewSet,
    PaginationParamsMixin,
    GetLibraryMixin,
    GetUserMixin,
):
    """Base class for browser viewsets."""

    filter_class: type[FilterSet]

    def get_queryset(self, request: Request) -> models.QuerySet:
        """Get queryset."""
        return self.filter_class()(request)


class PlaylistMetaViewSet(BaseBrowserViewSet):
    """Browser Playlist ViewSet.

    Returns a collection of statistics and metadata
    about playlists that have been persisted/synced
    to the database and associated with a user's library.
    """

    filter_class = PlaylistFilterSet
    relation: str = "playlists"
    authentication_classes = [SpotifyAuth]
    permission_classes = [IsAuthenticated]

    def list(self, request: Request) -> Response:
        """GET /playlists.

        Filters and returns a paginated list of playlists based
        on query parameters.
        """
        qs = Playlist.objects.filter(libraries__user_id=request.user.id)

        data = {
            "total_synced": qs.filter(is_synced=True).count(),
            "total_analyzed": qs.filter(is_analyzed=True).count(),
            "total_synced_tracks": qs.filter(is_synced=True)
            .aggregate(
                track_count=models.Count("tracks"),
            )
            .get("track_count"),
            "total_analyzed_tracks": qs.filter(is_analyzed=True)
            .aggregate(
                track_count=models.Count("tracks"),
            )
            .get("track_count"),
            "total_unanalyzed_tracks": qs.filter(is_analyzed=False)
            .aggregate(
                track_count=models.Count("tracks"),
            )
            .get("track_count"),
            "total_tracks": qs.aggregate(
                track_count=models.Count("tracks"),
            ).get("track_count"),
        }

        logger.info(f"Playlist metadata: {data}")

        return Response(data=data, status=status.HTTP_200_OK)


class PlaylistViewSet(BaseBrowserViewSet):
    """Browser (persisted) Playlist API Views.

    Query methods return filtered records of one or many
    playlists that have been persisted/synced to the database
    and associated with a user's library.

    Action methods dispatch tasks to sync or analyze playlists
    and their tracks.
    """

    filter_class = PlaylistFilterSet
    relation: str = "playlists"
    authentication_classes = [SpotifyAuth]
    permission_classes = [IsAuthenticated]

    def list(self, request: Request) -> Response:
        """GET /playlists.

        Filters and returns a paginated list of playlists based
        on query parameters.
        """
        qs = self.get_queryset(request)
        return Response(
            data=ListPlaylistSerializer.to_response(
                qs.all(),
                self.get_params(request),
            ),
            status=status.HTTP_200_OK,
        )

    def update(self, request: Request, playlist_pk: str, *args, **kwargs) -> Response:
        """PUT /playlists/{pk}.

        Does a complete update of a playlist, i.e. dispatches
        a celery group that syncs & then analyzes the playlist.
        """
        result = sync_and_analyze_playlist.s(
            uuid.UUID(playlist_pk), request.user.id
        ).apply_async()

        return Response(
            data=TaskResultSerializer.from_result(result).model_dump(),
            status=status.HTTP_202_ACCEPTED,
        )

    def partial_update(
        self, request: Request, playlist_pk: str, *args, **kwargs
    ) -> Response:
        """PATCH /playlists/{pk}.

        Partially updates a playlist, i.e. only syncs or analyzes
        the playlist. Defaults to sync.
        """
        if request.data.get("operation") == "analyze":
            result = analyze_playlist.s(playlist_pk, request.user.id).apply_async()
        else:
            result = sync_playlist.s(playlist_pk, request.user.id).apply_async()
        return Response(
            data=TaskResultSerializer.from_result(result).model_dump(),
            status=status.HTTP_202_ACCEPTED,
        )

    def create(self, request: Request) -> Response:
        """POST /playlists.

        Based on params (filtered queryset), this view dispatches
        a batch of celery tasks to analyze the playlists.
        """
        qs = self.get_queryset(request)
        params = self.get_params(request)
        objects = (
            Paginator(qs.all(), per_page=params.page_size)
            .page(
                params.page,
            )
            .object_list
        )

        result = group(
            *(
                sync_playlist.s(
                    playlist.id,
                    request.user.id,
                )
                for playlist in objects
            )
        ).apply_async()

        return Response(
            data=TaskResultSerializer.from_result(result).model_dump(),
            status=status.HTTP_202_ACCEPTED,
        )

    def retrieve(self, request: Request, playlist_pk: str, *args, **kwargs) -> Response:
        """GET /playlists/{pk}.

        Retrieves a single playlist by its primary key, and related
        objects:
            - tracks (paginated)
            - computation
        """
        playlist = (
            self.get_queryset(request)
            .prefetch_related(
                "tracks",
                "analysis",
                "tracks__album",
                "tracks__album__artists",
            )
            .get(id=uuid.UUID(playlist_pk))
        )

        return Response(
            data={**RetrievePlaylistSerializer.to_response(playlist)},
            status=status.HTTP_200_OK,
        )

    def destroy(self, request: Request, pk: str | None = None) -> Response:
        """Destroy a playlist."""
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


class AlbumViewSet(BaseBrowserViewSet):
    """Album ViewSet."""

    filter_class = AlbumFilterSet
    relation: str = "albums"
    authentication_classes = [SpotifyAuth]
    permission_classes = [IsAuthenticated]

    def list(self, request: Request) -> Response:
        """GET /albums.

        Filters and returns a paginated list of albums based
        on query parameters.
        """
        qs = self.get_queryset(request)
        return Response(
            data=ListAlbumSerializer.to_response(
                qs.all(),
                self.get_params(request),
            ),
            status=status.HTTP_200_OK,
        )

    def retrieve(self, request: Request, album_pk: str) -> Response:
        """GET /albums/{pk}.

        Retrieves a single album by its primary key.
        """
        album = (
            self.get_queryset(request)
            .prefetch_related("tracks", "artists")
            .get(
                id=uuid.UUID(album_pk),
            )
        )
        return Response(
            data={"data": RetrieveAlbumSerializer.get(album).model_dump()},
            status=status.HTTP_200_OK,
        )


class TrackViewSet(ViewSet):
    """Track ViewSet."""

    pass
