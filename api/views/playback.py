"""Playback data access views.

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

from api.serializers import playback
from api.views.base import SpotifyPlaybackView

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


class RecentlyPlayedView(SpotifyPlaybackView):
    """Get recently played tracks.

    Endpoint: GET /api/playback/recent
    """

    def get(self, request: DRFRequest) -> HttpResponse:
        """Get the last played track.

        Endpoint: GET /api/playback/last
        """
        limit = request.query_params.get("limit", 5)
        app_user = self.get_user(request)
        iterator = self.playback_service.recently_played(app_user, int(limit))
        data = list(iterator)
        recently_played = playback.RecentlyPlayed.list(data)

        return JsonResponse({"data": [track.model_dump() for track in recently_played]})


class LastPlayedView(SpotifyPlaybackView):
    """Get the last played track.

    Endpoint: GET /api/playback/last
    """

    def get(self, request: DRFRequest) -> HttpResponse:
        """Get the last played track.

        Endpoint: GET /api/playback/last
        """
        app_user = self.get_user(request)
        response = self.playback_service.recently_played(app_user, 1)

        for data in response:
            last_played = playback.RecentlyPlayed.get(data)

        return JsonResponse({"data": last_played.model_dump()})
