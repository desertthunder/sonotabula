"""Library data access views.

Parking Lot:
- TODO: Dispatch celery tasks for fetching data.
- TODO: Implement caching for data / sync v. async data fetching.
"""

import logging

from django.http import (
    HttpResponse,
    JsonResponse,
)
from rest_framework.request import Request as DRFRequest

from api.serializers import library
from api.views.base import SpotifyLibraryView

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class LibraryArtistsView(SpotifyLibraryView):
    """Get the user's artists."""

    def get(self, request: DRFRequest) -> HttpResponse:
        """Get the user's artists.

        Endpoint: GET /api/library/artists
        """
        limit = request.query_params.get("limit", 10)
        app_user = self.get_user(request)
        iterator = self.library_service.library_artists(app_user.pk, int(limit))
        response = list(iterator)
        data = library.Artist.list(response)
        return JsonResponse(data={"data": [artist.model_dump() for artist in data]})


class LibraryAlbumsView(SpotifyLibraryView):
    """Get the user's albums."""

    def get(self, request: DRFRequest) -> HttpResponse:
        """Get the user's albums.

        Endpoint: GET /api/library/albums
        """
        limit = request.query_params.get("limit", 10)
        app_user = self.get_user(request)
        iterator = self.library_service.library_albums(app_user.pk, int(limit))
        response = list(iterator)
        data = library.Album.list(response)
        return JsonResponse(data={"data": [album.model_dump() for album in data]})
