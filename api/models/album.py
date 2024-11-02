"""Album Model."""

import uuid

from django.db import models
from loguru import logger

from api.blocks import AlbumArtistSyncBlock, AlbumSyncBlock, AlbumTrackSyncBlock
from api.models.mixins import CanBeAnalyzedMixin, SpotifyModel, TimestampedModel


class AlbumSyncManager(models.Manager["Album"]):
    """Methods for syncing albums."""

    def _clean_track_data(self, data: dict) -> AlbumTrackSyncBlock:
        """Clean track data."""
        try:
            return AlbumTrackSyncBlock(
                **{
                    "name": data["name"],
                    "spotify_id": data["id"],
                    "duration": data["duration_ms"],
                }
            )
        except Exception as e:
            raise ValueError(f"Invalid track data: {e}") from e

    def _clean_artist_data(self, data: dict) -> AlbumArtistSyncBlock:
        """Clean artist data."""
        try:
            return AlbumArtistSyncBlock(
                **{
                    "name": data["name"],
                    "spotify_id": data["id"],
                }
            )
        except Exception as e:
            raise ValueError(f"Invalid artist data: {e}") from e

    def clean_data(self, data: dict) -> AlbumSyncBlock:
        """Clean API data."""
        try:
            tracks = [
                self._clean_track_data(track)
                for track in data.get("tracks", {}).get("items", []) or []
            ]

            artists = [
                self._clean_artist_data(artist)
                for artist in data.get("artists", []) or []
            ]

            release_date = data["release_date"]

            album_data = {
                "name": data["name"],
                "spotify_id": data["id"],
                "album_type": data["album_type"],
                "image_url": data["images"][0]["url"],
                "label": data["label"],
                "copyright": data["copyrights"][0]["text"],
                "release_year": int(release_date.split("-")[0]),
                "genres": data["genres"],
            }
            logger.debug(album_data)

            return AlbumSyncBlock(**album_data, artists=artists, tracks=tracks)

        except Exception as e:
            logger.error(e.__class__.__name__)
            logger.error(e)
            raise ValueError(f"Invalid data: {e}") from e

    def sync_data(self, cleaned: AlbumSyncBlock) -> "Album":
        """Sync album data."""
        album, _ = self.model.objects.update_or_create(
            spotify_id=cleaned.spotify_id,
            defaults={
                "name": cleaned.name,
                "album_type": cleaned.album_type,
                "image_url": cleaned.image_url,
                "label": cleaned.label,
                "release_year": cleaned.release_year,
                "is_synced": False,
                "copyright": cleaned.copyright,
            },
        )

        return album

    def complete_sync(self, album_id: uuid.UUID) -> uuid.UUID:
        """Complete sync operation."""
        album = self.model.objects.get(pk=album_id)
        album.is_synced = True
        album.save()

        return album.pk


class Album(SpotifyModel, TimestampedModel, CanBeAnalyzedMixin):
    """Album model.

    Required fields for creation:
        - name
        - spotify_id
    """

    album_type = models.CharField(max_length=255, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    copyright = models.CharField(max_length=255, blank=True, null=True)
    release_year = models.IntegerField()
    genres = models.ManyToManyField("api.Genre", related_name="albums")

    sync = AlbumSyncManager()
    objects = models.Manager()
