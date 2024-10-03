"""Service layer."""

import dataclasses
import logging
import os
import time
from http import HTTPMethod

import httpx
from httpx import URL, Request

from api.libs.constants import REDIRECT_URI, SpotifyAPIEndpoints, SpotifyAPIScopes
from api.libs.exceptions import MissingAPICredentialsError, SpotifyAPIError

logger = logging.getLogger("spotify_service")


# TODO: Move this to a utils module
def get_current_unix_timestamp() -> int:
    """Return the current Unix timestamp."""
    return int(time.time())


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
        """Return the data as a dictionary."""
        return dataclasses.asdict(self)


@dataclasses.dataclass
class SpotifyResponse:
    """Spotify Response Data base class."""

    @property
    def as_dict(self) -> dict:
        """Return the data as a dictionary."""
        return dataclasses.asdict(self)


@dataclasses.dataclass
class SpotifyAccessTokenRequest(SpotifyRequest):
    """Spotify Access Token Request Data."""

    code: str
    redirect_uri: str = REDIRECT_URI
    grant_type: str = "authorization_code"


@dataclasses.dataclass
class SpotifyAccessTokenResponse(SpotifyResponse):
    """Spotify Access Token Response Data."""

    access_token: str
    refresh_token: str
    token_type: str
    token_expiry: int

    def __init__(
        self, access_token: str, refresh_token: str, token_type: str, token_expiry: int
    ) -> None:
        """Spotify Access Token Response."""
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_type = token_type
        self.token_expiry = get_current_unix_timestamp() + token_expiry


@dataclasses.dataclass
class SpotifyRedirectParams(SpotifyRequest):
    """Spotify Redirect URL Parameters."""

    client_id: str
    state: str
    scope: str
    response_type: str = "code"
    redirect_uri: str = REDIRECT_URI


@dataclasses.dataclass
class SpotifyCurrentUserDataResponse(SpotifyResponse):
    """Spotify Current User Data."""

    display_name: str
    email: str
    id: str


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
        if self.client.is_closed:
            self.client = httpx.Client()

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
        if self.client.is_closed:
            self.client = httpx.Client()

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


class SpotifyDataService:
    """API actions for fetching data from the Spotify API."""

    pass
