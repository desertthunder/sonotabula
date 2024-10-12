"""Track model and manager."""

import typing
import uuid

from django.db import models
from pydantic import BaseModel

from api.models.music import Album, Artist, SpotifyModel, TimestampedModel


class SyncData(BaseModel):
    """Data for syncing."""

    artists: list["SyncArtist"]
    album: "SyncAlbum"
    track: "SyncTrack"


class SyncTrack(BaseModel):
    """Track data for syncing."""

    name: str
    spotify_id: str  # id
    duration: int  # duration_ms
    album_id: str  # album.id


class SyncAlbum(BaseModel):
    """Album data for syncing."""

    name: str
    spotify_id: str  # id
    release_year: int  # release_date
    image_url: str  # images[0].url
    artist_ids: list[str]  # artists[].id
    album_type: str  # album_type


class SyncArtist(BaseModel):
    """Artist data for syncing.

    Comes from track.artists & album.artists.
    """

    name: str
    spotify_id: str  # id


class TrackSyncManager(models.Manager["Track"]):
    """Sync tracks, albums, and artists."""

    def before_sync(self, items: typing.Iterable[dict]) -> typing.Iterable[SyncData]:
        """Before sync hook."""
        for item in items:
            track_data = item.get("track", {})
            album_data = track_data.get("album", {})
            artist_data = list(
                {
                    artist["id"]: artist
                    for artist in album_data.get("artists", [])
                    + track_data.get("artists", [])
                }.values()
            )

            track = SyncTrack(
                name=track_data.get("name"),
                spotify_id=track_data.get("id"),
                duration=track_data.get("duration_ms"),
                album_id=album_data.get("id"),
            )
            album_release_year = album_data.get("release_date").split("-")[0]

            album = SyncAlbum(
                name=album_data.get("name"),
                spotify_id=album_data.get("id"),
                release_year=int(album_release_year),
                image_url=album_data.get("images", [{}])[0].get("url"),
                album_type=album_data.get("album_type"),
                artist_ids=[artist["id"] for artist in album_data.get("artists", [])],
            )

            artists = [
                SyncArtist(
                    spotify_id=artist["id"],
                    name=artist["name"],
                )
                for artist in artist_data
            ]

            yield SyncData(
                track=track,
                album=album,
                artists=artists,
            )

    def sync(
        self, items: typing.Iterable[SyncData]
    ) -> typing.Iterable[tuple[uuid.UUID, str]]:
        """Sync tracks, albums, and artists.

        Dependency Tree:
            - Track
                - Album
                    - Artist
        """
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
                    "artists": album_artists,
                },
            )

            t, _ = self.model.objects.update_or_create(
                spotify_id=track.spotify_id,
                defaults={
                    "name": track.name,
                    "duration": track.duration,
                    "album": album_record,
                },
            )

            yield (t.pk, t.spotify_id)


class Track(SpotifyModel, TimestampedModel):
    """Track model.

    Required fields for creation:
        - name
        - spotify_id
    """

    duration = models.IntegerField()
    album = models.ForeignKey(
        "api.Album", related_name="tracks", on_delete=models.PROTECT, null=True
    )

    objects: models.Manager["Track"] = models.Manager()
    sync: TrackSyncManager = TrackSyncManager()
