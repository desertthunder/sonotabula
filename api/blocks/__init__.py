"""Models for validating data.

AlbumSyncBlock is a data validator block for album data
when syncing API data.
"""

from pydantic import BaseModel


class AlbumTrackSyncBlock(BaseModel):
    """Album track data validator block."""

    name: str
    spotify_id: str
    duration: int


class AlbumArtistSyncBlock(BaseModel):
    """Album artist data validator block."""

    name: str
    spotify_id: str


class AlbumSyncBlock(BaseModel):
    """Album data validator block."""

    name: str
    spotify_id: str
    album_type: str
    image_url: str
    label: str
    copyright: str
    release_year: int
    artists: list[AlbumArtistSyncBlock]
    tracks: list[AlbumTrackSyncBlock]
