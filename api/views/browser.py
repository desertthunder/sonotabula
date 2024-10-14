"""Browser views."""

from django.http import (
    HttpResponse,
    JsonResponse,
)
from rest_framework.request import Request as DRFRequest

from api.filters import PlaylistFilterSet
from api.filters.tracks import TrackFilterSet
from api.models.playlist import Playlist
from api.models.serializers import PlaylistModelSerializer, TrackModelSerializer
from api.views.base import BrowserView


class BrowserPlaylistTracksView(BrowserView):
    """Playlist tracks browser view."""

    filterset = TrackFilterSet()

    def get(
        self, request: DRFRequest, playlist_id: str, *args, **kwargs
    ) -> HttpResponse:
        """Get request."""
        records = self.filterset(
            request,
            playlist_pk=playlist_id,
            include_features=True,
            include_computations=True,
        )
        playlist = Playlist.objects.get(pk=playlist_id)
        data = TrackModelSerializer.list(records)
        return JsonResponse(
            data={
                "data": {
                    "playlist": PlaylistModelSerializer.get(playlist).model_dump(),
                    "tracks": [record.model_dump() for record in data],
                    "computations": [],
                }
            }
        )


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
