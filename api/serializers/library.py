"""Library serializers."""

from api.serializers.base import Serializer


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
    public: bool = False
    shared: bool = False
    description: str | None = None

    @classmethod
    def mappings(cls: type["Playlist"]) -> dict[str, str]:
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
    def nullable_fields(cls: type["Playlist"]) -> tuple:
        """Fields that can be null."""
        return (
            "description",
            "public",
            "collaborative",
        )

    @classmethod
    def get(cls: type["Playlist"], response: dict) -> "Playlist":
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

        return cls(**data)


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

    @classmethod
    def nullable_fields(cls: type["Album"]) -> tuple:
        """Fields that can be null."""
        return ("",)


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

    @classmethod
    def nullable_fields(cls: type["Track"]) -> tuple:
        """Fields that can be null."""
        return ("",)


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

    @classmethod
    def nullable_fields(cls: type["Artist"]) -> tuple:
        """Fields that can be null."""
        return ("",)
