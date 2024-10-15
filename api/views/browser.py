"""Browser views.

Parking Lot:
- (TODO): Reimplement paginator in /browser/playlists/:id/tracks
"""

from django.core.paginator import Paginator
from django.http import (
    HttpResponse,
    JsonResponse,
)
from rest_framework.request import Request as DRFRequest

from api.filters import AlbumFilterSet, PlaylistFilterSet, TrackFilterSet
from api.models.playlist import Playlist
from api.serializers.views import browser as responses
from api.views.base import BrowserView


# /browser/playlists/
class BrowserPlaylistView(BrowserView):
    """Playlist tracks browser view.

    GET /api/browser/playlists/{playlist_id}/tracks
    """

    filterset = None

    def get(
        self, request: DRFRequest, playlist_id: str, *args, **kwargs
    ) -> HttpResponse:
        """Get request."""
        playlist = (
            Playlist.objects.prefetch_related("analysis")
            .prefetch_related("tracks")
            .prefetch_related("tracks__features")
            .get(pk=playlist_id)
        )

        return JsonResponse(
            data=responses.ExpandedPlaylistSerializer.to_response(playlist)
        )


class BrowserPlaylistListView(BrowserView):
    """Get the user's persisted playlists.

    GET /api/browser/playlists
    """

    filterset = PlaylistFilterSet()

    def get(self, request: DRFRequest, *args, **kwargs) -> HttpResponse:
        """Get the user's playlists.

        Endpoint: GET /api/browser/playlists
        """
        page = request.query_params.get("page", 1)
        page_size = request.query_params.get("page_size", 10)
        records = self.filterset(request)
        paginator = Paginator(object_list=records, per_page=page_size)

        return JsonResponse(
            data=responses.PaginatedPlaylistListSerializer.from_paginator(
                paginator=paginator,
                page=int(page),
            ).model_dump()
        )


# /browser/tracks/
class BrowserTrackView(BrowserView):
    """Get a user's track."""

    pass


class BrowserTrackListView(BrowserView):
    """Get the user's persisted tracks."""

    filterset = TrackFilterSet()

    def get(self, request: DRFRequest, *args, **kwargs) -> HttpResponse:
        """Get the user's tracks.

        Endpoint: GET /api/browser/tracks
        """
        page = request.query_params.get("page", 1)
        page_size = request.query_params.get("page_size", 10)

        records = self.filterset(request)
        paginator = Paginator(object_list=records, per_page=page_size)

        return JsonResponse(
            data=responses.PaginatedTrackListSerializer.from_paginator(
                paginator=paginator,
                page=int(page),
            ).model_dump()
        )


# /browser/albums/
class BrowserAlbumView(BrowserView):
    """Get a user's album."""

    pass


class BrowserAlbumListView(BrowserView):
    """Get the user's persisted albums.

    GET /api/browser/albums
    """

    filterset = AlbumFilterSet()

    def get(self, request: DRFRequest, *args, **kwargs) -> HttpResponse:
        """Get the user's albums.

        Endpoint: GET /api/browser/albums
        """
        page = request.query_params.get("page", 1)
        page_size = request.query_params.get("page_size", 10)

        records = self.filterset(request)
        paginator = Paginator(object_list=records, per_page=page_size)

        return JsonResponse(
            data=responses.PaginatedAlbumListSerializer.from_paginator(
                paginator=paginator,
                page=int(page),
            ).model_dump()
        )
