"""Music Persistence Models.

Parking Lot
- (TODO) Musicbrainz integration models
"""

from django.db import models

from api.blocks import AlbumArtistSyncBlock
from api.models.album import Album
from api.models.mixins import CanBeSyncedMixin, SpotifyModel, TimestampedModel


class ArtistSyncManager(models.Manager["Artist"]):
    """Manager for syncing artists."""

    def sync_album_artist(
        self, album: Album, cleaned: AlbumArtistSyncBlock
    ) -> "Artist":
        """Sync album artist."""
        artist, _ = self.model.objects.update_or_create(
            spotify_id=cleaned.spotify_id,
            defaults={"name": cleaned.name},
        )

        artist.albums.add(album)

        return artist


class Artist(SpotifyModel, TimestampedModel, CanBeSyncedMixin):
    """Artist model.

    Required fields for creation:
        - name
        - spotify_id
    """

    image_url = models.URLField(blank=True, null=True)
    spotify_follower_count = models.IntegerField(blank=True, null=True)
    albums = models.ManyToManyField("api.Album", related_name="artists")
    genres = models.ManyToManyField("api.Genre", related_name="artists")

    sync = ArtistSyncManager()
    objects = models.Manager()


class Genre(TimestampedModel):
    """Genre model.

    Required fields for creation:
        - name
    """

    name = models.CharField(max_length=255, unique=True, null=False, blank=False)
