"""Browser ViewSets.

Primary viewsets for feature context collections.
These are audio features stored under a user's
"Library."
"""

import typing

from django.db import models
from loguru import logger
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from api.models.permissions import SpotifyAuth
from browser.filters import PlaylistFilterSet
from browser.models import Library
from browser.serializers import ListPlaylistSerializer, PaginationParams
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


class PlaylistViewSet(BaseBrowserViewSet):
    """Playlist viewset."""

    filter_class = PlaylistFilterSet
    relation: str = "playlists"
    authentication_classes = [SpotifyAuth]
    permission_classes = [IsAuthenticated]

    def list(self, request: Request) -> Response:
        """List all playlists."""
        qs = self.get_queryset(request)
        return Response(
            data=ListPlaylistSerializer.to_response(qs.all(), self.get_params(request)),
            status=status.HTTP_200_OK,
        )

    def create(self, request: Request) -> Response:
        """Create a playlist."""
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def retrieve(self, request: Request, pk: str | None = None) -> Response:
        """Retrieve a playlist."""
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def update(self, request: Request, pk: str | None = None) -> Response:
        """Update a playlist."""
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def destroy(self, request: Request, pk: str | None = None) -> Response:
        """Destroy a playlist."""
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


class AlbumViewSet(ViewSet):
    """Album ViewSet."""

    pass


class TrackViewSet(ViewSet):
    """Track ViewSet."""

    pass
