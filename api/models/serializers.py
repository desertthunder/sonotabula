"""Pydantic implementation of serializers."""

from pydantic import BaseModel


def map_response(response: dict, mappings: dict, nullable_fields: tuple) -> dict:
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

    for field in nullable_fields:
        if field not in data:
            data[field] = None  # type: ignore

    return data


class SimplePlaylist(BaseModel):
    """Proposed final playlist."""

    spotify_id: str
    owner_id: str
    name: str
    version: str
    image_url: str
    shared: bool | None = None
    public: bool | None = None
    description: str | None = None

    @classmethod
    def mappings(cls: type["SimplePlaylist"]) -> dict:
        """Mapping of JSON data to class properties."""
        return {
            "spotify_id": "id",
            "owner_id": "owner.id",
            "version": "snapshot_id",
            "image_url": "images.0.url",
            "name": "name",
        }

    @classmethod
    def nullable_fields(cls: type["SimplePlaylist"]) -> tuple:
        """Fields that can be null."""
        return (
            "description",
            "public",
        )

    @classmethod
    def build(cls: type["SimplePlaylist"], response: dict) -> "SimplePlaylist":
        """Create a SimplePlaylist object from JSON data."""
        data = map_response(response, cls.mappings(), cls.nullable_fields())

        data["shared"] = response.get("collaborative") or False
        data["public"] = response.get("public") or False

        return cls(**data)


class PlaylistTrack(BaseModel):
    """Track serializer."""

    spotify_id: str
    artist_ids: list[str]
    album_id: str
    name: str
    duration: int

    @classmethod
    def mappings(cls: type["PlaylistTrack"]) -> dict:
        """Mapping of JSON data to class properties."""
        return {
            "spotify_id": "track.id",
            "album_id": "track.album.id",
            "name": "track.name",
            "duration": "track.duration_ms",
        }

    @classmethod
    def build(cls: type["PlaylistTrack"], response: dict) -> "PlaylistTrack":
        """Create a PlaylistTrack object from JSON data."""
        data = map_response(response, cls.mappings(), ())

        artist_ids = [
            artist["id"] for artist in response.get("track", {}).get("artists", [])
        ]

        return cls(**data, artist_ids=artist_ids)


class PlaylistAlbum(BaseModel):
    """Album from track object."""

    spotify_id: str
    name: str
    image_url: str
    album_type: str
    release_year: str

    @classmethod
    def mappings(cls: type["PlaylistAlbum"]) -> dict:
        """Mapping of JSON data to class properties."""
        return {
            "spotify_id": "id",
            "name": "name",
            "image_url": "images.0.url",
            "album_type": "album_type",
            "release_year": "release_date",
        }

    @classmethod
    def build(cls: type["PlaylistAlbum"], response: dict) -> "PlaylistAlbum":
        """Create a PlaylistAlbum object from JSON data."""
        data = map_response(response, cls.mappings(), ())

        return cls(**data)


class TrackFeatures(BaseModel):
    """Deserialized Spotify track features."""

    acousticness: float
    danceability: float
    duration_ms: int
    energy: float
    instrumentalness: float
    key: int  # TODO: Pitch class notation enum
    liveness: float
    loudness: float
    mode: int  # 0 or 1 for major or minor
    speechiness: float
    tempo: float  # BPM
    time_signature: int  # 3 - 7 all over 4
    valence: float


class Artist(BaseModel):
    """Artist Serializer."""

    spotify_id: str
    name: str
    image_url: str
    spotify_follower_count: int
    genres: list[str] = []

    @classmethod
    def mappings(cls: type["Artist"]) -> dict:
        """Mapping of JSON data to class properties."""
        return {
            "spotify_id": "id",
            "name": "name",
            "image_url": "images.0.url",
            "spotify_follower_count": "followers.total",
            "genres": "genres",
        }

    @classmethod
    def build(cls: type["Artist"], response: dict) -> "Artist":
        """Create an Artist object from JSON data."""
        data = map_response(response, cls.mappings(), ())

        if response.get("genres") is not None or response.get("genres") == "":
            data["genres"] = []

        return cls(**data)
