"""Authentication service.

Parking lot:
- TODO: Get User Profile
"""

import os
from http import HTTPMethod

import httpx
from loguru import logger

from api.libs.constants import SpotifyAPIEndpoints, SpotifyAPIScopes
from api.libs.exceptions import MissingAPICredentialsError, SpotifyAPIError
from api.libs.params import SpotifyRedirectParams
from api.libs.requests import (
    SpotifyAccessTokenRequest,
    SpotifyRedirectURI,
    SpotifyRefreshTokenRequest,
)
from api.serializers.authentication import AccessToken, CurrentUser
from core.models import AppUser

logger.add("logs/spotify_auth.log", rotation="1 MB", retention="1 day", level="DEBUG")


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

    def get_access_token(self, code: str) -> AccessToken:
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

            if not resp.get("access_token"):
                raise SpotifyAPIError("Access token not found in response.")

            client.close()

        logger.debug(f"Access token response: {resp}")

        token_set = AccessToken.get(resp)

        logger.debug(f"Access token for expires at {token_set.token_expiry}")

        return token_set

    def get_current_user(self, access_token: str) -> CurrentUser:
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

            client.close()

        if not resp.get("display_name") or not resp.get("email") or not resp.get("id"):
            raise SpotifyAPIError("User data not found in response.")

        return CurrentUser.get(
            {
                "display_name": resp["display_name"],
                "email": resp["email"],
                "id": resp["id"],
            }
        )

    def get_full_profile(self, user_id: int) -> dict:
        """Fetch's current user's full profile."""
        try:
            user = AppUser.objects.get(id=user_id)
            client = httpx.Client(
                base_url=SpotifyAPIEndpoints.BASE_URL,
                headers={"Authorization": f"Bearer {user.access_token}"},
            )

            response = client.get(url=SpotifyAPIEndpoints.CurrentUser)

            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            if (
                exc.response.status_code == 401
                and "The access token expired" in exc.response.text
            ):
                user = self.refresh_access_token(user.refresh_token)
                client.headers["Authorization"] = f"Bearer {user.access_token}"

                response = client.get(url=SpotifyAPIEndpoints.CurrentUser)
                response.raise_for_status()
            else:
                client.close()
                raise exc
        finally:
            client.close()

        return response.json()

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

    def refresh_access_token(self, refresh_token: str) -> AppUser:
        """Refresh the access token and update the user's token set."""
        try:
            user = AppUser.objects.get(refresh_token=refresh_token)
        except AppUser.DoesNotExist as exc:
            logger.error(f"User not found with refresh token: {refresh_token}")

            raise SpotifyAPIError("User not found.") from exc

        request_data = SpotifyRefreshTokenRequest(refresh_token, self.client_id)  # type: ignore

        response = httpx.post(
            url=SpotifyAPIEndpoints.Access_Token,
            data=request_data.as_dict,
            auth=self.auth(),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        if response.is_error:
            logger.error(f"Error: {response.text}")

            raise SpotifyAPIError(response.text)

        resp = response.json()

        logger.debug(f"Response: {resp.keys()}")

        if not resp.get("access_token"):
            logger.error("Access token not found in response")

            raise SpotifyAPIError("Access token not found in response.")

        logger.debug(f"Access token response: {resp.get('access_token')[1:10]}...")

        token_set = AccessToken.get(
            {
                **resp,
                "refresh_token": resp.get("refresh_token", refresh_token),
            }
        )

        user = user.update_token_set(token_set)

        return user
