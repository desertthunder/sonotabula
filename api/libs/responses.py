"""Response data classes for the Spotify API."""

import dataclasses
import typing

from pydantic import BaseModel


# TODO: Remove
@dataclasses.dataclass
class SpotifyResponse:
    """Spotify Response Data base class."""

    @property
    def as_dict(self) -> dict:
        """Return the data as a dictionary."""
        return dataclasses.asdict(self)


# TODO: Remove
def map_response(response: dict, mappings: dict) -> dict:
    """Map JSON data to class properties."""
    data = {}

    for key, value in mappings.items():
        path = value.split(".")
        prop = response.copy()

        for p in path:
            if p.isdigit() and isinstance(prop, list):
                i = int(p)
                prop = prop[i]
            elif isinstance(prop, dict) and prop.get(p):
                prop = prop.get(p)  # type: ignore
        if isinstance(prop, dict):
            prop = ""  # type: ignore

        if prop is not None:
            data[key] = prop

    return data


# TODO: Remove
class Serializer(BaseModel):
    """Base class for serializing data."""

    @classmethod
    def mappings(cls: type["Serializer"]) -> dict[str, str]:
        """Mapping of JSON data to class properties."""
        raise NotImplementedError("Subclasses must implement this method.")

    @classmethod
    def get(cls: type["Serializer"], response: dict) -> "Serializer":
        """Create a Serializer object from JSON data."""
        data: dict = map_response(response, cls.mappings())

        return cls(**data)

    @classmethod
    def list(
        cls: type["Serializer"], response: list[dict]
    ) -> typing.Iterable["Serializer"]:
        """Create a list of Serializer objects from JSON data."""
        for item in response:
            yield cls.get(item)


# TODO: Remove
class RecentlyPlayed(Serializer):
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
    def mappings(cls: type["RecentlyPlayed"]) -> dict[str, str]:
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


# TODO: Remove
class Playlist(Serializer):
    """Playlist API response data."""

    spotify_id: str
    name: str
    owner_name: str
    owner_id: str
    link: str
    image_url: str
    num_tracks: int
    track_link: str
    version: str
    # public: bool = False
    # shared: bool = False
    description: str | None = None

    @classmethod
    def mappings(cls: type["Playlist"]) -> dict[str, str]:
        """Mapping of JSON data to class properties."""
        return {
            "spotify_id": "id",
            "name": "name",
            "description": "description",
            "version": "snapshot_id",
            # "public": "public",
            # "shared": "collaborative",
            "owner_name": "owner.display_name",
            "owner_id": "owner.id",
            "link": "external_urls.spotify",
            "image_url": "images.0.url",
            "num_tracks": "tracks.total",
            "track_link": "tracks.href",
        }


# TODO: Remove
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


# TODO: Remove
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


# TODO: Remove
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
