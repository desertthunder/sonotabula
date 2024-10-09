"""Data access views."""

import logging

from django.http import (
    HttpResponse,
    JsonResponse,
)
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request as DRFRequest

from api.libs.responses import (
    Album,
    Artist,
    Playlist,
    RecentlyPlayed,
    Track,
)
from api.models import AppUser
from api.models.permissions import SpotifyAuth
from api.services.spotify import SpotifyDataService

default_data_service = SpotifyDataService()  # NOTE used for dependency injection

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


class SpotifyDataView(views.APIView):
    """Base class for Spotify data views."""

    authentication_classes = [
        SpotifyAuth,
    ]
    permission_classes = [
        IsAuthenticated,
    ]

    data_service: SpotifyDataService

    def __init__(
        self, data_service: SpotifyDataService = default_data_service, *args, **kwargs
    ) -> None:
        """Validate View Constructor."""
        self.data_service = data_service

        super().__init__(*args, **kwargs)

    def get_user(self, request: DRFRequest) -> AppUser:
        """Get the user from the request."""
        return AppUser.objects.get(pk=request.user.pk)


class LastPlayedView(SpotifyDataView):
    """Get the last played track.

    Endpoint: GET /api/playback/last
    """

    def get(self, request: DRFRequest) -> HttpResponse:
        """Get the last played track.

        Endpoint: GET /api/playback/last
        """
        app_user = self.get_user(request)
        data = self.data_service.last_played(app_user)
        last_played = RecentlyPlayed.get(data[0])

        return JsonResponse(data=last_played.model_dump())


class RecentlyPlayedView(SpotifyDataView):
    """Get recently played tracks.

    Endpoint: GET /api/playback/recent
    """

    def get(self, request: DRFRequest) -> HttpResponse:
        """Get the last played track.

        Endpoint: GET /api/playback/last
        """
        limit = request.query_params.get("limit", 5)
        app_user = self.get_user(request)
        data = self.data_service.recently_played(app_user, int(limit))
        recently_played = RecentlyPlayed.list(data)

        return JsonResponse({"data": [rp.model_dump() for rp in recently_played]})


class LibraryPlaylistsView(SpotifyDataView):
    """Get the user's playlists."""

    def get(self, request: DRFRequest) -> HttpResponse:
        """Get the user's playlists.

        Endpoint: GET /api/library/playlists
        """
        limit = request.query_params.get("limit", 5)
        app_user = self.get_user(request)
        response = self.data_service.library_playlists(app_user, int(limit))
        data = Playlist.list(response)

        return JsonResponse(data={"data": [p.model_dump() for p in data]})


class LibraryArtistsView(SpotifyDataView):
    """Get the user's artists."""

    def get(self, request: DRFRequest) -> HttpResponse:
        """Get the user's artists.

        Endpoint: GET /api/library/artists
        """
        limit = request.query_params.get("limit", 5)
        app_user = self.get_user(request)
        response = self.data_service.library_artists(app_user, int(limit))
        data = Artist.list(response)

        return JsonResponse(data={"data": [a.model_dump() for a in data]})


class LibraryAlbumsView(SpotifyDataView):
    """Get the user's albums."""

    def get(self, request: DRFRequest) -> HttpResponse:
        """Get the user's albums.

        Endpoint: GET /api/library/albums
        """
        limit = request.query_params.get("limit", 5)
        app_user = self.get_user(request)
        response = self.data_service.library_albums(app_user, int(limit))
        data = Album.list(response)

        return JsonResponse(data={"data": [a.model_dump() for a in data]})


class LibraryTracksView(SpotifyDataView):
    """Get the user's tracks."""

    def get(self, request: DRFRequest) -> HttpResponse:
        """Get the user's tracks.

        Endpoint: GET /api/library/tracks
        """
        limit = request.query_params.get("limit", 5)
        app_user = self.get_user(request)
        response = self.data_service.library_tracks(app_user, int(limit))
        data = Track.list(response)
        return JsonResponse(data={"data": [t.model_dump() for t in data]})
