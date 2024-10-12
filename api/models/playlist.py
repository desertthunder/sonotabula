"""Playlist Model."""

import datetime
import typing
import uuid

from django.db import models
from django.utils import timezone
from django_stubs_ext.db.models import TypedModelMeta
from loguru import logger
from pydantic import BaseModel

from api.models.music import SpotifyModel, TimestampedModel


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


class SyncTrack(BaseModel):
    """Track data for syncing."""

    name: str
    spotify_id: str


class PlaylistSyncManager(models.Manager["Playlist"]):
    """Manager for syncing user playlists."""

    def pre_sync(self, playlists: typing.Iterable[dict]) -> list[SyncPlaylist]:
        """Validate API data and prepare for syncing."""
        result = []
        for playlist in playlists:
            logger.debug(playlist.get("id"))
            result.append(
                SyncPlaylist(
                    name=playlist.get("name", ""),
                    spotify_id=playlist.get("id", ""),
                    owner_id=playlist.get("owner", {}).get("id"),
                    version=playlist.get("snapshot_id"),
                    image_url=playlist.get("images", [{}])[0].get("url"),
                    public=playlist.get("public"),
                    shared=playlist.get("collaborative"),
                    description=playlist.get("description"),
                )
            )

        return result

    def do(self, playlists: list[SyncPlaylist], user_pk: int) -> list["Playlist"]:
        """Batch create playlists.

        Returns list of tuple of playlist pks and spotify ids.
        """
        added: list[Playlist] = self.bulk_create(
            (
                self.model(**playlist.model_dump(), user_id=user_pk)
                for playlist in playlists
            ),
            ignore_conflicts=True,
        )

        logger.debug(f"Added {len(added)} playlists.")
        for playlist in added:
            logger.debug(f"Added playlist {playlist.pk} | {playlist.spotify_id}.")
        logger.debug([playlist.spotify_id for playlist in playlists])

        return list(
            self.filter(
                spotify_id__in=[playlist.spotify_id for playlist in playlists]
            ).all()
        )

    def complete_sync(
        self, library_pk: int, playlists: list["Playlist"]
    ) -> list[tuple[uuid.UUID, str]]:
        """Complete playlist sync.

        Sets is_synced to True and adds library to playlists.
        """
        updated = []

        for playlist in playlists:
            playlist.is_synced = True
            playlist.libraries.add(library_pk)
            playlist.save()

            logger.debug(f"Added playlist {playlist.pk} to library {library_pk}.")

            updated.append((playlist.pk, playlist.spotify_id))

        return updated


class Playlist(SpotifyModel, TimestampedModel):
    """Spotify playlist model.

    Required fields for creation:
        - name
        - spotify_id
        - owner_id
    """

    version = models.CharField(max_length=255, blank=True, null=True)  # snapshot_id
    image_url = models.URLField(blank=True, null=True)
    public = models.BooleanField(null=True, blank=True)
    shared = models.BooleanField(null=True, blank=True)  # collaborative
    description = models.TextField(blank=True, null=True)
    owner_id = models.CharField(max_length=255, null=False, blank=False)
    is_synced = models.BooleanField(default=False, null=True, blank=True)
    is_analyzed = models.BooleanField(default=False, null=True, blank=True)

    user = models.ForeignKey(
        "api.AppUser", related_name="playlists", on_delete=models.PROTECT, null=True
    )

    libraries = models.ManyToManyField("api.Library", related_name="playlists")

    objects: models.Manager["Playlist"] = models.Manager()
    sync = PlaylistSyncManager()

    @property
    def stale_data(self) -> bool:
        """Check if playlist data is more than a week old."""
        return self.updated_at < timezone.now() - datetime.timedelta(days=7)

    class Meta(TypedModelMeta):
        """Playlist model metadata."""

        ordering = ["-is_synced", "-updated_at", "-is_analyzed", "-created_at"]
        unique_together = ["spotify_id", "user"]
