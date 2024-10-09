"""Response data classes for the Spotify API."""

import dataclasses
import datetime
import typing

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
        data: dict = {}

        if not response:
            return cls(**response)  # We're relying on BaseModel to raise an error here.

        for key, value in cls.get_mapping().items():
            path = value.split(".")
            prop: dict | str | list = response.copy()

            for p in path:
                if p.isdigit() and isinstance(prop, list):
                    i = int(p)
                    prop = prop[i]
                elif isinstance(prop, dict) and prop.get(p):
                    prop = prop.get(p)  # type: ignore

            data[key] = prop

        return cls(**data)

    @classmethod
    def serialize_from_json(cls: type["LastPlayed"], response: dict) -> dict:
        """Serialize JSON data to a dictionary."""
        obj = cls.from_json(response)
        return obj.model_dump()


class RecentlyPlayed(LastPlayed):
    """Recently played API response data.

    The service uses the same endpoint as the LastPlayed response.
    """

    @classmethod
    def from_json_collection(
        cls: type["RecentlyPlayed"], response: list[dict]
    ) -> typing.Iterator["RecentlyPlayed"]:
        """Create a RecentlyPlayed object from JSON data."""
        for item in response:
            yield cls(**cls.serialize_from_json(item))


class Serializer(BaseModel):
    """Base class for serializing data."""

    @classmethod
    def mappings(cls: type["Serializer"]) -> dict[str, str]:
        """Mapping of JSON data to class properties."""
        raise NotImplementedError("Subclasses must implement this method.")

    @classmethod
    def get(cls: type["Serializer"], response: dict) -> "Serializer":
        """Create a Serializer object from JSON data."""
        data: dict = {}

        for key, value in cls.mappings().items():
            path = value.split(".")
            prop: dict | str | list = response.copy()

            for p in path:
                if p.isdigit() and isinstance(prop, list):
                    i = int(p)
                    prop = prop[i]
                elif isinstance(prop, dict) and prop.get(p):
                    prop = prop.get(p)  # type: ignore
            data[key] = prop

        return cls(**data)

    @classmethod
    def list(
        cls: type["Serializer"], response: list[dict]
    ) -> typing.Iterable["Serializer"]:
        """Create a list of Serializer objects from JSON data."""
        for item in response:
            yield cls.get(item)


class Playlist(Serializer):
    """Playlist API response data."""

    spotify_id: str
    name: str
    description: str
    owner_name: str
    owner_id: str
    link: str
    image_url: str
    num_tracks: int

    @classmethod
    def mappings(cls: type["Playlist"]) -> dict[str, str]:
        """Mapping of JSON data to class properties."""
        return {
            "spotify_id": "id",
            "name": "name",
            "description": "description",
            "owner_name": "owner.display_name",
            "owner_id": "owner.id",
            "link": "external_urls.spotify",
            "image_url": "images.0.url",
            "num_tracks": "tracks.total",
        }


class Album(Serializer):
    """Album API response data."""

    spotify_id: str
    name: str
    artist_name: str
    artist_id: str
    release_date: str
    total_tracks: int
    image_url: str

    @classmethod
    def mappings(cls: type["Album"]) -> dict[str, str]:
        """Mapping of JSON data to class properties."""
        return {
            "spotify_id": "album.id",
            "name": "album.name",
            "artist_name": "album.artists.0.name",
            "artist_id": "album.artists.0.id",
            "release_date": "album.release_date",
            "total_tracks": "album.total_tracks",
            "image_url": "album.images.0.url",
        }


class Track(Serializer):
    """Track API response data."""

    spotify_id: str
    name: str
    artist_name: str
    artist_id: str
    album_name: str
    album_id: str
    duration_ms: int
    link: str

    @classmethod
    def mappings(cls: type["Track"]) -> dict[str, str]:
        """Mapping of JSON data to class properties."""
        return {
            "spotify_id": "track.id",
            "name": "track.name",
            "artist_name": "track.artists.0.name",
            "artist_id": "track.artists.0.id",
            "album_name": "track.album.name",
            "album_id": "track.album.id",
            "duration_ms": "track.duration_ms",
            "link": "track.external_urls.spotify",
        }


class Artist(Serializer):
    """Artist API response data."""

    genres: list[str]
    spotify_id: str
    name: str
    link: str
    image_url: str

    @classmethod
    def mappings(cls: type["Artist"]) -> dict[str, str]:
        """Mapping of JSON data to class properties."""
        return {
            "genres": "genres",
            "spotify_id": "id",
            "name": "name",
            "link": "external_urls.spotify",
            "image_url": "images.0.url",
        }
