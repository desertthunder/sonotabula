"""Library serializers."""

from pydantic import BaseModel, Field

from api.models import Playlist as PlaylistModel


class PlaylistTrack(BaseModel):
    """Playlist track serializer."""

    # track.id
    spotify_id: str
    # track.name
    name: str
    # album.id
    album_id: str
    # album.name
    album_name: str
    # album.album_type
    album_type: str
    # artists[].id, artists[].name
    artists: list[tuple[str, str]]
    # duration_ms
    duration_ms: int
    # external_ids.isrc
    isrc: str | None = None


class ExpandedPlaylist(BaseModel):
    """Expanded playlist serializer."""

    # id
    spotify_id: str
    collaborative: bool
    description: str
    # external_urls.spotify
    spotify_link: str
    # images.0.url
    image_url: str
    name: str
    # owner.id, owner.display_name
    owner: tuple[str, str]
    public: bool
    snapshot_id: str
    # followers.total
    follower_count: int
    id: str | int | None = None

    tracks: list[PlaylistTrack] = Field(default_factory=list)

    @classmethod
    def get(cls: type["ExpandedPlaylist"], response: dict) -> "ExpandedPlaylist":
        """Create an ExpandedPlaylist object from JSON data."""
        playlist: ExpandedPlaylist = ExpandedPlaylist.model_construct()

        if playlist_data := response.get("playlist"):
            playlist = ExpandedPlaylist(
                spotify_id=playlist_data.get("id"),
                collaborative=playlist_data.get("collaborative"),
                description=playlist_data.get("description"),
                spotify_link=playlist_data.get("external_urls", {}).get("spotify"),
                image_url=playlist_data.get("images", [{}])[0].get("url"),
                name=playlist_data.get("name"),
                owner=(
                    playlist_data.get("owner", {}).get("id"),
                    playlist_data.get("owner", {}).get("display_name"),
                ),
                public=playlist_data.get("public"),
                snapshot_id=playlist_data.get("snapshot_id"),
                follower_count=playlist_data.get("followers", {}).get("total"),
                tracks=[],
            )
        else:
            raise ValueError("Invalid playlist data.")

        tracks: list[PlaylistTrack] = []

        if track_data := response.get("tracks"):
            for item in track_data:
                item = item.get("track", {})
                track_data = item.get("track", {})

                artists = [
                    (artist.get("id", ""), artist.get("name", ""))
                    for artist in item.get("artists", [])
                ]
                tracks.append(
                    PlaylistTrack(
                        spotify_id=item.get("id"),
                        name=item.get("name"),
                        album_id=item.get("album", {}).get("id"),
                        album_name=item.get("album", {}).get("name"),
                        album_type=item.get("album", {}).get("album_type"),
                        artists=artists,
                        duration_ms=item.get("duration_ms"),
                        isrc=item.get("external_ids", {}).get("isrc"),
                    )
                )

        playlist.tracks.extend(tracks)

        if record := PlaylistModel.objects.filter(
            spotify_id=playlist.spotify_id
        ).first():
            playlist.id = str(record.id)

        return playlist
