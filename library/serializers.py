"""LIBRARY: Serializers for API data."""

import typing

from pydantic import BaseModel

from api.models import Artist, Playlist, Track
from browser.models import Library


class APISerializer(BaseModel):
    """Base class for serializing data."""

    @classmethod
    def mappings(cls: type[typing.Self]) -> dict[str, str]:
        """Mapping of JSON data to class properties."""
        raise NotImplementedError("Subclasses must implement this method.")

    @classmethod
    def nullable_fields(cls: type[typing.Self]) -> tuple:
        """Fields that can be null."""
        raise NotImplementedError("Subclasses must implement this method.")

    @classmethod
    def map_response(cls: type[typing.Self], response: dict) -> dict:
        """Map JSON data to class properties."""
        data = {}

        for key, value in cls.mappings().items():
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

        for field in cls.nullable_fields():
            if field not in data:
                data[field] = None  # type: ignore

        return data

    @classmethod
    def get(
        cls: type[typing.Self], response: dict, library: Library | None = None
    ) -> typing.Self:
        """Create a Serializer object from JSON data."""
        data: dict = cls.map_response(response)

        return cls(**data)

    @classmethod
    def list(
        cls: type[typing.Self], response: list[dict], library: Library | None = None
    ) -> typing.Iterable[typing.Self]:
        """Create a list of Serializer objects from JSON data."""
        for item in response:
            yield cls.get(item, library)


class PlaylistAPISerializer(APISerializer):
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
    public: bool = False
    shared: bool = False
    description: str | None = None
    id: str | int | None = None
    is_synced: bool = False

    @classmethod
    def mappings(cls: type["PlaylistAPISerializer"]) -> dict[str, str]:
        """Mapping of JSON data to class properties."""
        return {
            "spotify_id": "id",
            "name": "name",
            "version": "snapshot_id",
            "owner_name": "owner.display_name",
            "owner_id": "owner.id",
            "link": "external_urls.spotify",
            "image_url": "images.0.url",
            "num_tracks": "tracks.total",
            "track_link": "tracks.href",
        }

    @classmethod
    def nullable_fields(cls: type["PlaylistAPISerializer"]) -> tuple:
        """Fields that can be null."""
        return (
            "description",
            "public",
            "collaborative",
        )

    @classmethod
    def get(
        cls: type["PlaylistAPISerializer"],
        response: dict,
        library: Library | None = None,
    ) -> "PlaylistAPISerializer":
        """Create a Playlist object from JSON data."""
        data = cls.map_response(response)

        is_public = response.get("public")
        is_shared = response.get("collaborative")

        if is_public == "":
            data["public"] = False
        elif is_public is not None:
            data["public"] = is_public

        if is_shared == "":
            data["shared"] = False
        elif is_shared is not None:
            data["shared"] = is_shared

        if library is not None and (
            record := library.playlists.filter(spotify_id=data["spotify_id"]).first()
        ):
            data["is_synced"] = record.is_synced
            data["id"] = str(record.id)

        return cls(**data)

    def to_db(self) -> Playlist:
        """Convert a Playlist object to a PlaylistModel object."""
        pl, _ = Playlist.objects.update_or_create(
            spotify_id=self.spotify_id,
            owner_id=self.owner_id,
            defaults={
                "name": self.name,
                "image_url": self.image_url,
                "version": self.version,
                "public": self.public,
                "shared": self.shared,
                "description": self.description,
                "is_synced": self.is_synced,
            },
        )

        return pl


class AlbumAPISerializer(APISerializer):
    """Album API response data."""

    spotify_id: str
    name: str
    artist_name: str
    artist_id: str
    release_date: str
    total_tracks: int
    image_url: str
    label: str | None = None
    genres: list[str] | None = None
    id: str | int | None = None
    is_synced: bool = False

    @classmethod
    def mappings(cls: type["AlbumAPISerializer"]) -> dict[str, str]:
        """Mapping of JSON data to class properties."""
        return {
            "spotify_id": "album.id",
            "name": "album.name",
            "artist_name": "album.artists.0.name",
            "artist_id": "album.artists.0.id",
            "release_date": "album.release_date",
            "total_tracks": "album.tracks.total",
            "image_url": "album.images.0.url",
        }

    @classmethod
    def nullable_fields(cls: type["AlbumAPISerializer"]) -> tuple:
        """Fields that can be null."""
        return (
            "label",
            "genres",
        )

    @classmethod
    def get(
        cls: type["AlbumAPISerializer"], response: dict, library: Library | None = None
    ) -> "AlbumAPISerializer":
        """Serialize album."""
        data = cls.map_response(response)

        if library is not None and (
            record := library.albums.filter(spotify_id=data["id"]).first()
        ):
            data["is_synced"] = record.is_synced
            data["id"] = str(record.id)

        return cls(**data)


class TrackAPISerializer(APISerializer):
    """Track API response data."""

    spotify_id: str
    name: str
    artist_name: str
    artist_id: str
    album_name: str
    album_id: str
    album_release_date: str
    image_url: str
    duration_ms: int
    link: str
    id: str | None = None
    is_synced: bool = False
    is_analyzed: bool = False

    @classmethod
    def mappings(cls: type["TrackAPISerializer"]) -> dict[str, str]:
        """Mapping of JSON data to class properties."""
        return {
            "spotify_id": "track.id",
            "name": "track.name",
            "artist_name": "track.artists.0.name",
            "artist_id": "track.artists.0.id",
            "album_name": "track.album.name",
            "album_id": "track.album.id",
            "album_release_date": "track.album.release_date",
            "image_url": "track.album.images.0.url",
            "duration_ms": "track.duration_ms",
            "link": "track.external_urls.spotify",
        }

    @classmethod
    def nullable_fields(cls: type["TrackAPISerializer"]) -> tuple:
        """Fields that can be null."""
        return ("",)

    @classmethod
    def get(
        cls: type["TrackAPISerializer"], response: dict, *args, **kwargs
    ) -> "TrackAPISerializer":
        """Create a Track object from JSON data."""
        data = cls.map_response(response)

        if record := Track.objects.filter(spotify_id=data["spotify_id"]).first():
            data["is_synced"] = record.is_synced
            data["is_analyzed"] = record.is_analyzed
            data["id"] = str(record.id)

        return cls(**data)


class ArtistAPISerializer(APISerializer):
    """Artist API response data."""

    genres: list[str]
    spotify_id: str
    name: str
    link: str
    image_url: str
    id: str | None = None
    is_synced: bool = False

    @classmethod
    def mappings(cls: type["ArtistAPISerializer"]) -> dict[str, str]:
        """Mapping of JSON data to class properties."""
        return {
            "genres": "genres",
            "spotify_id": "id",
            "name": "name",
            "link": "external_urls.spotify",
            "image_url": "images.0.url",
        }

    @classmethod
    def nullable_fields(cls: type["ArtistAPISerializer"]) -> tuple:
        """Fields that can be null."""
        return ("",)

    @classmethod
    def get(
        cls: type["ArtistAPISerializer"], response: dict, *args, **kwargs
    ) -> "ArtistAPISerializer":
        """Create an Artist object from JSON data."""
        data = cls.map_response(response)

        if record := Artist.objects.filter(spotify_id=data["spotify_id"]).first():
            data["id"] = str(record.id)
            data["is_synced"] = record.is_synced

        if data.get("genres") is None or data.get("genres") == "":
            data["genres"] = ["N/A"]

        return cls(**data)


class TrackFeaturesAPISerializer(BaseModel):
    """Track Features model serializer."""

    id: str
    danceability: float
    energy: float
    key: int
    loudness: float
    mode: int
    speechiness: float
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float
    tempo: float
    duration_ms: int
    time_signature: int

    @classmethod
    def get(
        cls: type["TrackFeaturesAPISerializer"], data: dict
    ) -> "TrackFeaturesAPISerializer":
        """Create a model serializer from a model."""
        return cls(**data)
