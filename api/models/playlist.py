"""Playlist Model."""

import typing
import uuid

from django.db import models
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

    def before_sync(
        self, playlists: typing.Iterable[dict]
    ) -> typing.Iterable[SyncPlaylist]:
        """Validate API data and prepare for syncing."""
        for playlist in playlists:
            yield SyncPlaylist(
                name=playlist.get("name", ""),
                spotify_id=playlist.get("id", ""),
                owner_id=playlist.get("owner", {}).get("id"),
                version=playlist.get("snapshot_id"),
                image_url=playlist.get("images", [{}])[0].get("url"),
                public=playlist.get("public"),
                shared=playlist.get("collaborative"),
                description=playlist.get("description"),
            )

    def sync(
        self, playlists: typing.Iterable[SyncPlaylist], user_pk: int
    ) -> typing.Iterable[tuple[uuid.UUID, str]]:
        """Batch create playlists.

        Returns list of tuple of playlist pks and spotify ids.
        """
        synced: list[Playlist] = self.bulk_create(
            (
                self.model(**playlist.model_dump(), user_id=user_pk)
                for playlist in playlists
            ),
            ignore_conflicts=True,
        )

        synced_spotify_ids = [playlist.spotify_id for playlist in synced]
        existing = self.filter(spotify_id__in=synced_spotify_ids).values_list(
            "pk", "spotify_id"
        )

        yield from existing


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

    user = models.ForeignKey(
        "api.AppUser", related_name="playlists", on_delete=models.PROTECT, null=True
    )

    tracks = models.ManyToManyField("api.Track", related_name="playlists")

    objects: models.Manager["Playlist"] = models.Manager()
    sync = PlaylistSyncManager()
