"""Authentication views.

TODO - move these views to core
TODO - these views can be encapsulated in a single
ViewSet class
"""

from http import HTTPMethod

import httpx
import jwt
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    JsonResponse,
)
from django.shortcuts import redirect
from loguru import logger
from rest_framework import views
from rest_framework.request import Request as DRFRequest

from api.libs.constants import WEB_APP_URL, SpotifyAPIStates
from api.libs.exceptions import SpotifyAPIError
from api.libs.requests import RedirectURI
from api.models.permissions import Token
from api.services.spotify import AUTH, SpotifyAuthService
from core.models import AppUser
from server import settings


class SpotifyAuthView(views.APIView):
    """Spotify Authentication view base class."""

    _auth: SpotifyAuthService

    def __init__(
        self, auth_service: SpotifyAuthService = AUTH, *args, **kwargs
    ) -> None:
        """Validate View Constructor."""
        self._auth = auth_service

        super().__init__(*args, **kwargs)


class LoginView(SpotifyAuthView):
    """Login View."""

    def get(self, request: DRFRequest) -> HttpResponse:
        """Spotify Callback.

        Endpoint: GET /api/login
        """
        logger.debug("Received a GET request to /api/login")

        authorization_code: str | None = request.query_params.get("code")
        state = request.query_params.get("state")

        if (
            state != SpotifyAPIStates.LOGIN
            or not authorization_code
            or request.query_params.get("error") is not None
        ):
            return HttpResponseForbidden()

        try:
            token_set = self._auth.get_access_token(authorization_code)
        except SpotifyAPIError as exc:
            logger.error(f"Spotify API Error details: {exc}")

            return HttpResponseBadRequest("Unable to get access token.")

        try:
            current_user = self._auth.get_current_user(token_set.access_token)
        except SpotifyAPIError as exc:
            logger.error(f"Spotify API Error details: {exc}")

            return HttpResponseBadRequest("Unable to get current user.")

        user = AppUser.objects.from_spotify(current_user, token_set)
        client_jwt = Token(user)

        client = httpx.Client(base_url=WEB_APP_URL)

        req = client.build_request(
            HTTPMethod.GET,
            url="/dashboard",
            params={"token": client_jwt.encode()},  # NOTE can be used to look up user.
        )

        resp = redirect(to=RedirectURI.from_request(req))
        resp.headers["Access-Control-Allow-Origin"] = "*"

        logger.debug("Redirecting to dashboard.")

        return resp

    def post(self, request: DRFRequest) -> HttpResponse:
        """Login to Spotify.

        Endpoint: POST /api/login
        """
        redirect_uri = self._auth.build_redirect_uri()

        resp = redirect(to=redirect_uri)
        resp.headers["Access-Control-Allow-Origin"] = "*"

        logger.debug("Redirecting to Spotify for login.")
        logger.debug(f"Headers: {resp.headers}")

        return JsonResponse(data={"redirect": resp.url})


class ValidateView(SpotifyAuthView):
    """Validate View.

    Polled by the client to check if the JWT token is still valid.

    Endpoint: GET /api/validate
    """

    def refresh_token(self, user: AppUser) -> str:
        """Refresh the token."""
        user = self._auth.refresh_access_token(user.refresh_token)
        client_jwt = Token(user)
        return client_jwt.encode()

    def post(self, request: DRFRequest) -> HttpResponse:
        """Validate the JWT token.

        Endpoint: POST /api/validate
        """
        token = request.headers.get("Authorization")

        if not token:
            return HttpResponseForbidden()

        tag, token = token.split(" ")

        if tag.lower() != "bearer":
            return HttpResponseForbidden()

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            logger.debug(
                f"Invalid or expired token for user {payload.get('public_id')}"
            )
            return HttpResponseForbidden()

        logger.debug(f"Found token for user {payload.get('public_id')}")

        try:
            user = AppUser.objects.get(public_id=payload.get("public_id"))

            logger.debug(f"Found user: {user.public_id} with pk {user.pk}")
        except AppUser.DoesNotExist:
            logger.error("User not found.")

            return HttpResponseForbidden(content={"message": "User not found."})

        if user.token_expired:
            logger.debug("Token expired. Refreshing token.")

            try:
                updated_jwt = self.refresh_token(user)

                return JsonResponse(
                    data={"message": "Updated token", "token": updated_jwt}
                )
            except SpotifyAPIError as exc:
                logger.error(f"Spotify API Error details: {exc}")

                return HttpResponseBadRequest("Unable to refresh token.")

        return JsonResponse(data={"message": "Valid token.", "token": token})
