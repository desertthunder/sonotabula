"""Spotify API Request Dataclasses."""

import dataclasses

from httpx import URL, Request

from api.libs.constants import REDIRECT_URI


@dataclasses.dataclass
class RedirectURI:
    """Redirect URI wrapper."""

    _url: URL

    @classmethod
    def from_request(cls: type["RedirectURI"], request: Request) -> str:
        """Create a RedirectURI from a Request."""
        return cls(_url=request.url).as_str

    @property
    def as_str(self) -> str:
        """Return the URL as a string."""
        return str(self._url)


@dataclasses.dataclass
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
