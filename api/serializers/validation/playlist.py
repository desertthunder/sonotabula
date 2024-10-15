"""Playlist validation serializers.

These serializers are used to validate incoming data for playlist creation.
"""

from pydantic import BaseModel


class SyncPlaylist(BaseModel):
    """Playlist data for syncing."""

    name: str
    spotify_id: str
    owner_id: str
    version: str | None = None
    image_url: str | None = None
    public: bool | None = None
    shared: bool | None = None
    description: str | None = None
