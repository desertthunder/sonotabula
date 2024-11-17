"""Custom Permissions class implementation for REST Framework.

In order to allow unauthenticated access to the Spotify
API callback, we need to make a custom permission class.
"""

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from core.models import AppUser
from core.serializers import TokenSerializer


class SpotifyAuth(BaseAuthentication):
    """Spotify Authentication."""

    def authenticate(self, request: Request) -> tuple[AppUser, str]:
        """Authenticate the request and return a two-tuple of (user, token)."""
        if "Authorization" in request.headers:
            user_email = self.authenticate_header(request)
            user = AppUser.objects.get(email=user_email)

            return user, user.access_token

        raise AuthenticationFailed("Authentication credentials were not provided.")

    def authenticate_header(self, request: Request) -> str | None:
        """Decodes the JWT token and returns the payload."""
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
            payload = TokenSerializer.get_payload(token)

            return payload.email
        raise AuthenticationFailed("Authentication credentials were not provided.")


class AllowCallbackUnauthenticated(BasePermission):
    """Allow unauthenticated access to the Spotify API callback."""

    def has_permission(self, request: Request, view: APIView | ViewSet) -> bool:
        """Check that the action is refers to the callback."""
        if isinstance(view, ViewSet) and view.action in ["api-callback", "create"]:
            return True
        else:
            return bool(request.user and request.user.is_authenticated)
