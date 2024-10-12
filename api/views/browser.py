"""Browser views."""

from django.http import (
    HttpResponse,
    JsonResponse,
)
from rest_framework.request import Request as DRFRequest

from api.filters import PlaylistFilterSet
from api.models.serializers import PlaylistModelSerializer
from api.views.base import BrowserView


class BrowserPlaylistTracksView(BrowserView):
    """Playlist tracks browser view."""

    def get(self, request: DRFRequest, *args, **kwargs) -> HttpResponse:
        """Get request."""
        raise NotImplementedError


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
