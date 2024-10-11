"""Data Serializers."""

import typing

from pydantic import BaseModel

from api.serializers.base import Serializer


class PlaylistData(Serializer):
    """Individual playlist."""

    collaborative: bool
    id: str
    name: str
    snapshot_id: str
    owner_id: str
    image_url: str
    public: bool | None
    description: str | None

    @classmethod
    def mappings(cls: type["PlaylistData"]) -> dict[str, str]:
        """Mapping of JSON data to class properties."""
        return {
            "collaborative": "collaborative",
            "spotify_id": "id",
            "name": "name",
            "snapshot_id": "snapshot_id",
            "owner_id": "owner.id",
            "image_url": "images.0.url",
        }

    @classmethod
    def nullable_fields(cls: type["PlaylistData"]) -> tuple:
        """Fields that can be null."""
        return ("description", "public")


class UserSavedItems(BaseModel):
    """User saved item totals."""

    artists: int
    albums: int
    tracks: int
    playlists: int
    shows: int

    @classmethod
    def get(
        cls: type["UserSavedItems"], iter: typing.Iterable[tuple[str, dict]]
    ) -> "UserSavedItems":
        """Get user saved items."""
        response = {
            "artists": 0,
            "albums": 0,
            "tracks": 0,
            "playlists": 0,
            "shows": 0,
        }

        for item, data in iter:
            key = item.split("/")[-1]

            if key == "following":
                response["artists"] = data["total"]
            else:
                response[key] = data["total"]

        return cls(**response)
