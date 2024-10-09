"""Response data classes for the Spotify API."""

import dataclasses
import datetime

from django.utils import timezone
from pydantic import BaseModel


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


class LastPlayed(BaseModel):
    """Last played API response data."""

    album_name: str
    album_link: str
    album_art_url: str

    track_name: str
    track_link: str

    artist_name: str
    artist_link: str

    played_at: str

    @classmethod
    def get_mapping(cls: type["LastPlayed"]) -> dict[str, str]:
        """Mapping of JSON data to class properties."""
        return {
            "album_name": "track.album.name",
            "album_link": "track.album.external_urls.spotify",
            "album_art_url": "track.album.images.0.url",
            "track_name": "track.name",
            "track_link": "track.external_urls.spotify",
            "artist_name": "track.artists.0.name",
            "artist_link": "track.artists.0.external_urls.spotify",
            "played_at": "played_at",
        }

    @classmethod
    def from_json(cls: type["LastPlayed"], response: dict) -> "LastPlayed":
        """Create a LastPlayed object from JSON data."""
        resp: dict = {}

        data = response.get("items")

        if not data:
            raise ValueError("Items not found in response.")

        if not data[0].get("track"):
            raise ValueError("Track not found in response.")

        data = data[0]

        for key, value in cls.get_mapping().items():
            path = value.split(".")
            prop: dict | str | list = data

            for p in path:
                if p.isdigit() and isinstance(prop, list):
                    i = int(p)
                    prop = prop[i]
                elif isinstance(prop, dict) and prop.get(p):
                    prop = prop.get(p)  # type: ignore

            resp[key] = prop

        return cls(**resp)
