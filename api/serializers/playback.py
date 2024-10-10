"""Playback serializers.

Last played and recently played (history) data.

Parking Lot:
- TODO: Create a database model for recently played data.
"""

from api.serializers.base import Serializer


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

    @classmethod
    def nullable_fields(cls: type["RecentlyPlayed"]) -> tuple[str]:
        """Fields that can be null."""
        return ("",)
