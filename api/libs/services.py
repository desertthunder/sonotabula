"""Service layer."""

import dataclasses
import logging
import os
from http import HTTPMethod

import httpx
from httpx import URL, Request

from api.libs.constants import REDIRECT_URI, SpotifyAPIEndpoints, SpotifyAPIScopes
from api.libs.exceptions import MissingAPICredentialsError, SpotifyAPIError
from api.libs.responses import (
    SpotifyAccessTokenResponse,
    SpotifyCurrentUserDataResponse,
)
from api.models import AppUser

logger = logging.getLogger("spotify_service")


# TODO: Move this to a utils module


class RedirectURI:
    """Redirect URI wrapper."""

    _url: URL

    def __init__(self, url: URL) -> None:
        """Redirect URI Constructor."""
        self._uri = url

    @classmethod
    def from_request(cls: type["RedirectURI"], request: Request) -> str:
        """Create a RedirectURI from a Request."""
        return cls(url=request.url).as_str

    @property
    def as_str(self) -> str:
        """Return the URL as a string."""
        return str(self._uri)


class SpotifyRedirectURI(RedirectURI):
    """Spotify Redirect URI wrapper."""

    pass


@dataclasses.dataclass
class SpotifyRequest:
    """Spotify Request Data base class."""

    @property
    def as_dict(self) -> dict:
        """Return the dataclass as a dictionary."""
        return dataclasses.asdict(self)


@dataclasses.dataclass
class SpotifyAccessTokenRequest(SpotifyRequest):
    """Spotify Access Token Request Data."""

    code: str
    redirect_uri: str = REDIRECT_URI
    grant_type: str = "authorization_code"


@dataclasses.dataclass
class SpotifyRefreshTokenRequest(SpotifyRequest):
    """Spotify Refresh Token Request Data."""

    refresh_token: str
    client_id: str
    grant_type: str = "refresh_token"


@dataclasses.dataclass
class SpotifyRedirectParams(SpotifyRequest):
    """Spotify Redirect URL Parameters."""

    client_id: str
    state: str
    scope: str
    response_type: str = "code"
    redirect_uri: str = REDIRECT_URI


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
            response = client.get(url=SpotifyAPIEndpoints.Current_User)

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

    def refresh_access_token(
        self, refresh_token: str | None = None, user: AppUser | None = None
    ) -> tuple[bool, AppUser | None]:
        """Refresh the access token and update the user's token set."""
        if not user and not refresh_token:
            return False, None

        if not refresh_token and user:
            refresh_token = user.refresh_token

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

        return True, user


class SpotifyDataService:
    """API actions for fetching data from the Spotify API."""

    def now_playing(self) -> None:
        """Get the user's currently playing track."""
        pass

    def recently_played(self) -> None:
        """Get the user's recently played tracks."""
        pass

    def top_tracks(self) -> None:
        """Get the user's top tracks."""
        pass
