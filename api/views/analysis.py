"""Basic analysis views."""

from django.http import HttpResponse, JsonResponse
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request as DRFRequest

from api.models import AppUser
from api.models.permissions import SpotifyAuth
from api.services.spotify import SpotifyAnalysisService

default_service = SpotifyAnalysisService()  # NOTE used for dependency injection


class PlaylistAnalysisView(views.APIView):
    """Base class for Spotify data views."""

    authentication_classes = [
        SpotifyAuth,
    ]
    permission_classes = [
        IsAuthenticated,
    ]

    service: SpotifyAnalysisService

    def __init__(
        self, service: SpotifyAnalysisService = default_service, *args, **kwargs
    ) -> None:
        """Validate View Constructor."""
        self.service = service

        super().__init__(*args, **kwargs)

    def get_user(self, request: DRFRequest) -> AppUser:
        """Get the user from the request."""
        return AppUser.objects.get(pk=request.user.pk)

    def get(self, request: DRFRequest, playlist_id: str) -> HttpResponse:
        """Get the last played track.

        Endpoint: GET /api/playback/last
        """
        app_user = self.get_user(request)
        data = self.service.expand_playlist(playlist_id, app_user)

        return JsonResponse(data=data.model_dump())
