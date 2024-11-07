"""Playback serializers."""

import typing

from pydantic import BaseModel


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
