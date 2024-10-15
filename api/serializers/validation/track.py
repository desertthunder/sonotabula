"""Track sync manager and models validators."""

from pydantic import BaseModel


class SyncTrackData(BaseModel):
    """Data for syncing."""

    artists: list["SyncTrackArtist"]
    album: "SyncTrackAlbum"
    track: "SyncTrack"


class SyncTrack(BaseModel):
    """Track data for syncing."""

    name: str
    spotify_id: str  # id
    duration: int  # duration_ms
    album_id: str  # album.id


class SyncTrackAlbum(BaseModel):
    """Album data for syncing."""

    name: str
    spotify_id: str  # id
    release_year: int  # release_date
    image_url: str  # images[0].url
    artist_ids: list[str]  # artists[].id
    album_type: str  # album_type


class SyncTrackArtist(BaseModel):
    """Artist data for syncing.

    Comes from track.artists & album.artists.
    """

    name: str
    spotify_id: str  # id
