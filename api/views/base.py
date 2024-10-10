"""API View base classes."""

from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request as DRFRequest

from api.models import AppUser
from api.models.permissions import SpotifyAuth
from api.services.spotify import SpotifyLibraryService, SpotifyPlaybackService

# NOTE used for dependency injection
default_playback_service = SpotifyPlaybackService()
default_library_service = SpotifyLibraryService()


class GetUserMixin:
    """Mixin for getting the user from the request."""

    def get_user(self, request: DRFRequest) -> AppUser:
        """Get the user from the request."""
        return AppUser.objects.get(pk=request.user.pk)


class SpotifyLibraryView(GetUserMixin, views.APIView):
    """Base class for Spotify data views."""

    authentication_classes = [
        SpotifyAuth,
    ]
    permission_classes = [
        IsAuthenticated,
    ]

    library_service: SpotifyLibraryService

    def __init__(
        self,
        library_service: SpotifyLibraryService = default_library_service,
        *args,
        **kwargs,
    ) -> None:
        """Validate View Constructor."""
        self.library_service = library_service

        super().__init__(*args, **kwargs)

    def get_user(self, request: DRFRequest) -> AppUser:
        """Get the user from the request."""
        return AppUser.objects.get(pk=request.user.pk)


class SpotifyPlaybackView(GetUserMixin, views.APIView):
    """Base class for Spotify playback views."""

    authentication_classes = [SpotifyAuth]
    permission_classes = [IsAuthenticated]

    playback_service: SpotifyPlaybackService

    def __init__(
        self,
        playback_service: SpotifyPlaybackService = default_playback_service,
        *args,
        **kwargs,
    ) -> None:
        """Validate View Constructor."""
        self.playback_service = playback_service

        super().__init__(*args, **kwargs)
