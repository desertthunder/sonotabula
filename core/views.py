"""Core API Views."""

from http import HTTPMethod, HTTPStatus

import httpx
import jwt
from django.http import HttpResponse
from django.shortcuts import redirect
from loguru import logger
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from api.libs.constants import SpotifyAPIStates
from api.libs.exceptions import SpotifyAPIError
from api.services.spotify import AUTH, DATA, SpotifyAuthService, SpotifyDataService
from core.models import AccessToken, AppUser
from core.permissions import AllowCallbackUnauthenticated, SpotifyAuth
from core.serializers import (
    RedirectURI,
    TokenSerializer,
    UserProfileSerializer,
    UserSavedItemSerializer,
)
from server import settings


class GetUserMixin:
    """Mixin for getting the user from the request."""

    def get_user(self, request: Request) -> AppUser:
        """Get the user from the request object.

        This method ensures that we're not using an
        AnonymousUser instance, as the QuerySet will
        raise a AppUser.DoesNotExist exception if we do.
        """
        return AppUser.objects.get(pk=request.user.pk)


class AuthenticationViewSet(viewsets.ViewSet):
    """User authentication view set."""

    permission_classes = [AllowAny]
    _auth: SpotifyAuthService = AUTH

    @action(name="api-callback", detail=False, methods=["GET"])
    def api_callback(self, request: Request) -> HttpResponse:
        """Generate a redirect URI to obtain a auth code.

        This is the callback URL for the registered application.
        """
        authorization_code: str | None = request.query_params.get("code")
        state = request.query_params.get("state")

        if (
            state != SpotifyAPIStates.LOGIN
            or not authorization_code
            or request.query_params.get("error") is not None
        ):
            return Response(
                data={"error": "Missing authorization code."},
                status=HTTPStatus.FORBIDDEN,
            )

        try:
            token_data = self._auth.get_access_token(authorization_code)
            tokens = AccessToken.get(token_data)

            spotify_data = self._auth.fetch_user(
                access_token=tokens.access_token, refresh_token=tokens.refresh_token
            )

            user = AppUser.objects.from_spotify(spotify_data, token_data)

            token = TokenSerializer.from_user(user)
            client = httpx.Client(base_url=settings.WEB_APP_URL)

            req = client.build_request(
                HTTPMethod.GET,
                url="/dashboard",
                params={"token": token.encode()},
            )

            resp = redirect(to=RedirectURI.from_request(req).url)
            resp.headers["Access-Control-Allow-Origin"] = "*"
            return resp
        except SpotifyAPIError as exc:
            logger.error(f"Spotify API Error details: {exc}")

            return Response(
                data={"error": "Unable to get current user."},
                status=HTTPStatus.BAD_REQUEST,
            )

    def create(self, request: Request) -> Response:
        """Create a redirect URI."""
        return Response(
            data={"redirect": self._auth.build_redirect_uri()},
            status=HTTPStatus.OK,
        )

    def update(self, request: Request) -> Response:
        """Refresh a user's tokens."""
        try:
            token = request.headers.get("Authorization")
            tag, token = token.split(" ") if token else (None, None)

            if not (tag and token) or tag.lower() != "bearer":
                raise ValueError("Invalid token format.")

            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

            user = AppUser.objects.get(public_id=payload.get("public_id"))
            user = self._auth.refresh_access_token(user.refresh_token)

            return Response(
                data={
                    "message": "Token refreshed.",
                    "token": TokenSerializer.from_user(user).encode(),
                },
                status=HTTPStatus.OK,
            )
        except (ValueError, jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return Response(
                data={"message": "Invalid or expired token."},
                status=HTTPStatus.BAD_REQUEST,
            )
        except AppUser.DoesNotExist:
            return Response(
                data={"message": "User not found."},
                status=HTTPStatus.NOT_FOUND,
            )
        except SpotifyAPIError:
            return Response(
                data={"message": "Unable to refresh token."},
                status=HTTPStatus.BAD_REQUEST,
            )


class ProfileViewSet(viewsets.ViewSet):
    """User profile view set."""

    authentication_classes = [SpotifyAuth]
    permission_classes = [AllowCallbackUnauthenticated]

    _auth: SpotifyAuthService = AUTH
    _data: SpotifyDataService = DATA

    def get_user(self, request: Request) -> AppUser:
        """Get the current user."""
        return AppUser.objects.get(id=request.user.id)

    def retrieve(self, request: Request) -> Response:
        """Get a user profile."""
        user = self.get_user(request)

        if user.should_update or bool(request.query_params.get("force", False)):
            saved_resp = self._data.fetch_saved_items(user)
            saved = UserSavedItemSerializer.get(saved_resp)

            profile_resp = self._auth.get_full_profile(user.pk)
            profile = UserProfileSerializer.from_api(profile_resp, user)
            profile = profile.update_counts(saved)
            profile.to_db(user)

            user.refresh_from_db()

        return Response(
            data={"data": UserProfileSerializer.from_db(user).model_dump()},
            status=HTTPStatus.OK,
        )

    def partial_update(self, request: Request, pk: int) -> Response:
        """Update a user's profile."""
        return Response(
            data={"message": "Partial update not allowed."},
            status=HTTPStatus.METHOD_NOT_ALLOWED,
        )
