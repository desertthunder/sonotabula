"""Spotify Request Params."""

import dataclasses

from api.libs.constants import REDIRECT_URI


@dataclasses.dataclass
class RequestParams:
    """Request Params base class."""

    path_params: list[str] = dataclasses.field(default_factory=list)

    @property
    def q(self) -> str:
        """Build and return the query string."""
        return ""

    @property
    def as_dict(self) -> dict:
        """Return the dataclass as a dictionary."""
        return dataclasses.asdict(self)


@dataclasses.dataclass
class SpotifyRedirectParams:
    """Spotify Redirect URL Parameters."""

    client_id: str
    state: str
    scope: str
    response_type: str = "code"
    redirect_uri: str = REDIRECT_URI

    @property
    def as_dict(self) -> dict:
        """Return the dataclass as a dictionary."""
        return dataclasses.asdict(self)

    @property
    def as_query_string(self) -> str:
        """Build and return the query string."""
        return "&".join([f"{key}={value}" for key, value in self.as_dict.items()])
