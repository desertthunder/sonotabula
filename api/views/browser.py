"""Browser views."""

from django.core.paginator import Paginator
from django.http import (
    HttpResponse,
    JsonResponse,
)
from loguru import logger
from rest_framework.request import Request as DRFRequest

from api.filters import PlaylistFilterSet
from api.filters.tracks import TrackFilterSet
from api.models.analysis import Analysis, Computation
from api.models.serializers import (
    PlaylistModelSerializer,
    TrackModelSerializer,
)
from api.views.base import BrowserView


class BrowserPlaylistTracksView(BrowserView):
    """Playlist tracks browser view."""

    filterset = TrackFilterSet()

    def get(
        self, request: DRFRequest, playlist_id: str, *args, **kwargs
    ) -> HttpResponse:
        """Get request."""
        page = request.query_params.get("page", 1)
        analysis = (
            Analysis.objects.prefetch_related("playlist")
            .prefetch_related("tracks")
            .get(playlist_id=playlist_id)
        )

        playlist = analysis.playlist
        computation = Computation.objects.get(analysis=analysis)
        tracks = analysis.tracks.prefetch_related("features").all()

        data = TrackModelSerializer.from_paginator(
            Paginator(object_list=tracks, per_page=5),
            page=int(page),
            playlist=playlist,
            computation=computation,
        )

        logger.info(data)

        return JsonResponse(data={**data})


class BrowserPlaylistView(BrowserView):
    """Get the user's persisted playlists."""

    filterset = PlaylistFilterSet()

    def get(self, request: DRFRequest, *args, **kwargs) -> HttpResponse:
        """Get the user's playlists.

        Endpoint: GET /api/browser/playlists
        """
        records = self.filterset(request)
        data = PlaylistModelSerializer.list(records)
        return JsonResponse(data={"data": [record.model_dump() for record in data]})
