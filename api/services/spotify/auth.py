"""Authentication service."""

import logging
import os
from http import HTTPMethod

import httpx

from api.libs.constants import SpotifyAPIEndpoints, SpotifyAPIScopes
from api.libs.exceptions import MissingAPICredentialsError, SpotifyAPIError
from api.libs.params import SpotifyRedirectParams
from api.libs.requests import (
    SpotifyAccessTokenRequest,
    SpotifyRedirectURI,
    SpotifyRefreshTokenRequest,
)
from api.libs.responses import (
    SpotifyAccessTokenResponse,
    SpotifyCurrentUserDataResponse,
)
from api.models import AppUser

logger = logging.getLogger("spotify_auth_service")


class SpotifyAuthService:
    """API actions for authorizing the Spotify API."""

    client: httpx.Client
    client_id: str | None
    client_secret: str | None

    def __init__(self) -> None:
        """Spotify Auth Service."""
        self.client = httpx.Client()

        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    def auth(self) -> httpx.BasicAuth:
        """Basic Auth for Spotify API."""
        if not self.client_id:
            raise MissingAPICredentialsError

        if not self.client_secret:
            raise MissingAPICredentialsError

        return httpx.BasicAuth(self.client_id, self.client_secret)

    def get_access_token(self, code: str) -> SpotifyAccessTokenResponse:
        """Handle the Spotify callback.

        Returns the access token, refresh token, and expiry time.

        Raises:
            SpotifyAPIError: If an error occurs with the Spotify API.
        """
        request_data = SpotifyAccessTokenRequest(code)

        with httpx.Client(
            base_url=SpotifyAPIEndpoints.Access_Token, auth=self.auth()
        ) as client:
            response = client.post(url="", data=request_data.as_dict)

            if response.is_error:
                logger.error(f"Error: {response.text}")

                raise SpotifyAPIError(response.text)

            resp = response.json()

            logger.debug(f"Response: {resp}")

            if not resp.get("access_token"):
                raise SpotifyAPIError("Access token not found in response.")

            client.close()

        logger.debug(f"Access token response: {resp}")

        token_set = SpotifyAccessTokenResponse(
            access_token=resp["access_token"],
            refresh_token=resp["refresh_token"],
            token_type=resp["token_type"],
            token_expiry=resp["expires_in"],
        )

        logger.debug(f"Access token for expires at {token_set.token_expiry}")

        return token_set

    def get_current_user(self, access_token: str) -> SpotifyCurrentUserDataResponse:
        """Get the current user's data."""
        with httpx.Client(
            base_url=SpotifyAPIEndpoints.BASE_URL,
            headers={"Authorization": f"Bearer {access_token}"},
        ) as client:
            response = client.get(url=SpotifyAPIEndpoints.CurrentUser)

            if response.is_error:
                logger.error(f"Error: {response.text}")

                raise SpotifyAPIError(response.text)

            resp = response.json()

            logger.debug(f"Response: {resp}")

            client.close()

        if not resp.get("display_name") or not resp.get("email") or not resp.get("id"):
            raise SpotifyAPIError("User data not found in response.")

        return SpotifyCurrentUserDataResponse(
            display_name=resp["display_name"],
            email=resp["email"],
            id=resp["id"],
        )

    def build_redirect_uri(self) -> str:
        """Build the Spotify authorization URL."""
        if not self.client_id:
            raise MissingAPICredentialsError

        params = SpotifyRedirectParams(
            client_id=self.client_id,
            state="app-login",
            scope=SpotifyAPIScopes.user_scopes(),
        )

        client = httpx.Client(base_url=SpotifyAPIEndpoints.Authorization)

        req = client.build_request(HTTPMethod.GET, url="", params=params.as_dict)

        return SpotifyRedirectURI.from_request(req)

    def refresh_access_token(self, refresh_token: str) -> tuple[bool, AppUser | None]:
        """Refresh the access token and update the user's token set."""
        try:
            user = AppUser.objects.get(refresh_token=refresh_token)
        except AppUser.DoesNotExist:
            return False, None

        request_data = SpotifyRefreshTokenRequest(refresh_token, self.client_id)  # type: ignore

        with httpx.Client(
            base_url=SpotifyAPIEndpoints.Access_Token, auth=self.auth()
        ) as client:
            response = client.post(url="", data=request_data.as_dict)

            if response.is_error:
                logger.error(f"Error: {response.text}")

                raise SpotifyAPIError(response.text)

            resp = response.json()
            logger.debug(f"Response: {resp}")

            if not resp.get("access_token"):
                return False, None

            client.close()

        logger.debug(f"Access token response: {resp}")

        token_set = SpotifyAccessTokenResponse(
            access_token=resp["access_token"],
            refresh_token=resp.get("refresh_token", user.refresh_token),
            token_type=resp["token_type"],
            token_expiry=resp["expires_in"],
        )

        user.update_token_set(token_set)
        user.refresh_from_db()

        return True, user
