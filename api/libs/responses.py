"""Response data classes for the Spotify API."""

import dataclasses
import datetime

from django.utils import timezone


@dataclasses.dataclass
class SpotifyResponse:
    """Spotify Response Data base class."""

    @property
    def as_dict(self) -> dict:
        """Return the data as a dictionary."""
        return dataclasses.asdict(self)


@dataclasses.dataclass
class SpotifyAccessTokenResponse(SpotifyResponse):
    """Spotify Access Token Response Data."""

    access_token: str
    refresh_token: str
    token_type: str
    token_expiry: datetime.datetime

    def __init__(
        self, access_token: str, refresh_token: str, token_type: str, token_expiry: int
    ) -> None:
        """Spotify Access Token Response."""
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_type = token_type
        self.token_expiry = timezone.now() + datetime.timedelta(seconds=token_expiry)


@dataclasses.dataclass
class SpotifyCurrentUserDataResponse(SpotifyResponse):
    """Spotify Current User Data."""

    display_name: str
    email: str
    id: str
