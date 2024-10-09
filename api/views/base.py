"""API View base classes."""

from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request as DRFRequest

from api.models import AppUser
from api.models.permissions import SpotifyAuth
from api.services.spotify import SpotifyDataService

default_data_service = SpotifyDataService()  # NOTE used for dependency injection


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
