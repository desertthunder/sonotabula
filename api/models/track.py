"""Track model and manager."""

import typing
import uuid

from django.db import models
from django.utils import timezone
from loguru import logger

from api.models.mixins import CanBeAnalyzedMixin
from api.models.music import Album, Artist, SpotifyModel, TimestampedModel
from api.serializers import validation


class TrackSyncManager(models.Manager["Track"]):
    """Sync tracks, albums, and artists."""

    def pre_sync(
        self, items: list[dict] | typing.Iterable[dict]
    ) -> list["validation.SyncTrackData"]:
        """Before sync hook."""
        cleaned = []
        for item in items:
            track_data = item.get("track", {})

            if track_data.get("type") in ("show", "episode"):
                logger.warning(
                    f"Skipping {track_data.get("id")} due to type"
                    f"{track_data.get('type')}"
                )

                continue

            album_data = track_data.get("album", {})
            artist_data = list(
                {
                    artist["id"]: artist
                    for artist in album_data.get("artists", [])
                    + track_data.get("artists", [])
                }.values()
            )

            track = validation.SyncTrack(
                name=track_data.get("name"),
                spotify_id=track_data.get("id"),
                duration=track_data.get("duration_ms"),
                album_id=album_data.get("id"),
            )

            album_release_year = (
                album_data.get("release_date").split("-")[0]
                if album_data.get("release_date")
                else None
            )

            album = validation.SyncTrackAlbum(
                name=album_data.get("name"),
                spotify_id=album_data.get("id"),
                release_year=int(album_release_year)
                if album_release_year
                else timezone.now().year,
                image_url=album_data.get("images", [{}])[0].get("url"),
                album_type=album_data.get("album_type"),
                artist_ids=[artist["id"] for artist in album_data.get("artists", [])],
            )

            artists = [
                validation.SyncTrackArtist(
                    spotify_id=artist.get("id"),
                    name=artist.get("name", "Unknown Artist"),
                )
                for artist in artist_data
            ]

            cleaned.append(
                validation.SyncTrackData(
                    track=track,
                    album=album,
                    artists=artists,
                )
            )

        return cleaned

    def do(
        self, items: list["validation.SyncTrackData"]
    ) -> list[tuple[uuid.UUID, str]]:
        """Sync tracks, albums, and artists.

        Dependency Tree:
            - Track
                - Album
                    - Artist
        """
        data = []
        for cleaned_data in items:
            artists = cleaned_data.artists
            album = cleaned_data.album
            track = cleaned_data.track

            Artist.objects.bulk_create(
                (
                    Artist(
                        name=artist.name,
                        spotify_id=artist.spotify_id,
                    )
                    for artist in artists
                ),
                ignore_conflicts=True,
            )

            album_artists = Artist.objects.filter(spotify_id__in=album.artist_ids)

            album_record, _ = Album.objects.update_or_create(
                spotify_id=album.spotify_id,
                defaults={
                    "name": album.name,
                    "release_year": album.release_year,
                    "image_url": album.image_url,
                    "album_type": album.album_type,
                },
            )

            for artist in album_artists:
                artist.albums.add(album_record)

            t, _ = self.model.objects.update_or_create(
                spotify_id=track.spotify_id,
                defaults={
                    "name": track.name,
                    "duration": track.duration,
                    "album": album_record,
                },
            )

            data.append((t.pk, t.spotify_id))

        return data

    def complete_sync(
        self, playlist_pk: uuid.UUID, data: list[tuple[uuid.UUID, str]]
    ) -> uuid.UUID:
        """Complete sync."""
        for track_id, _ in data:
            track = self.model.objects.get(pk=track_id)
            track.playlists.add(playlist_pk)  # type: ignore

        return playlist_pk


class Track(SpotifyModel, TimestampedModel, CanBeAnalyzedMixin):
    """Track model.

    Required fields for creation:
        - name
        - spotify_id
    """

    duration = models.IntegerField()
    album = models.ForeignKey(
        "api.Album", related_name="tracks", on_delete=models.PROTECT, null=True
    )
    playlists = models.ManyToManyField("api.Playlist", related_name="tracks")

    objects: models.Manager["Track"] = models.Manager()
    sync: TrackSyncManager = TrackSyncManager()

    @property
    def spotify_url(self) -> str:
        """Spotify URL."""
        return f"https://open.spotify.com/track/{self.spotify_id}"

    class Meta:
        """Track Meta options."""

        ordering = ["-is_analyzed", "-is_synced", "-created_at", "-updated_at"]
