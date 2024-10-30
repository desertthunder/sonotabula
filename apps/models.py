"""Spotify data access models."""

import datetime
import uuid

import pytz
from django.db import models
from django_stubs_ext.db.models import TypedModelMeta
from pydantic import BaseModel

from api.models.music import Album, Artist
from api.models.track import Track


class ListeningHistorySerializer(BaseModel):
    """Listening history serializer."""

    class NestedArtist(BaseModel):
        """Artist serializer."""

        spotify_id: str
        name: str

        @classmethod
        def from_api(
            cls: type["ListeningHistorySerializer.NestedArtist"], item: dict
        ) -> "ListeningHistorySerializer.NestedArtist":
            """Convert API data to serializer data."""
            return cls(
                spotify_id=item["id"],
                name=item["name"],
            )

        @classmethod
        def from_db(
            cls: type["ListeningHistorySerializer.NestedArtist"], data: "Artist"
        ) -> "ListeningHistorySerializer.NestedArtist":
            """Convert DB data to serializer data."""
            return cls(
                spotify_id=data.spotify_id,
                name=data.name,
            )

    class NestedAlbum(BaseModel):
        """Album serializer."""

        spotify_id: str
        name: str
        release_date: str
        image_url: str | None

        @classmethod
        def from_api(
            cls: type["ListeningHistorySerializer.NestedAlbum"], item: dict
        ) -> "ListeningHistorySerializer.NestedAlbum":
            """Convert API data to serializer data."""
            return cls(
                spotify_id=item["id"],
                name=item["name"],
                release_date=item["release_date"].split("-")[0],
                image_url=item["images"][0]["url"] if item.get("images") else None,
            )

        @classmethod
        def from_db(
            cls: type["ListeningHistorySerializer.NestedAlbum"], data: "Album"
        ) -> "ListeningHistorySerializer.NestedAlbum":
            """Convert DB data to serializer data."""
            return cls(
                spotify_id=data.spotify_id,
                name=data.name,
                release_date=str(data.release_year),
                image_url=data.image_url,
            )

    class NestedTrack(BaseModel):
        """Track serializer."""

        spotify_id: str
        name: str
        duration: int

        @classmethod
        def from_api(
            cls: type["ListeningHistorySerializer.NestedTrack"], item: dict
        ) -> "ListeningHistorySerializer.NestedTrack":
            """Convert API data to serializer data."""
            return cls(
                spotify_id=item["id"],
                name=item["name"],
                duration=item["duration_ms"],
            )

        @classmethod
        def from_db(
            cls: type["ListeningHistorySerializer.NestedTrack"], data: "Track"
        ) -> "ListeningHistorySerializer.NestedTrack":
            """Convert DB data to serializer data."""
            return cls(
                spotify_id=data.spotify_id,
                name=data.name,
                duration=data.duration,
            )

    id: str | None
    played_at: str
    track: NestedTrack
    album: NestedAlbum
    artists: list[NestedArtist]
    image_url: str | None

    @classmethod
    def from_api(
        cls: type["ListeningHistorySerializer"], item: dict
    ) -> "ListeningHistorySerializer":
        """Convert API data to serializer data."""
        data = item.get("track")
        if not data:
            raise ValueError("No track data found.")

        return cls(
            **{
                "id": None,
                "played_at": item["played_at"],
                "track": cls.NestedTrack.from_api(data).model_dump(),
                "album": cls.NestedAlbum.from_api(data["album"]).model_dump(),
                "artists": [
                    cls.NestedArtist.from_api(artist).model_dump()
                    for artist in data["artists"]
                ],
                "image_url": data["album"]["images"][0]["url"],
            }
        )

    @classmethod
    def from_db(
        cls: type["ListeningHistorySerializer"], data: "ListeningHistory"
    ) -> "ListeningHistorySerializer":
        """Convert DB data to serializer data."""
        track = cls.NestedTrack.from_db(data.track)

        if track_album := data.track.album:
            album = cls.NestedAlbum.from_db(track_album)

            artists = [
                cls.NestedArtist.from_db(artist) for artist in track_album.artists.all()
            ]

        return cls(
            id=str(data.id),
            played_at=data.played_at.astimezone(
                pytz.timezone("US/Central"),
            ).strftime("%Y-%m-%d %H:%M:%S %Z"),
            track=track,
            album=album,
            artists=artists,
            image_url=album.image_url,
        )


class ListeningHistoryManager(models.Manager["ListeningHistory"]):
    """Query manager for history models."""

    def get_full(self, pk: uuid.UUID | str) -> "ListeningHistory":
        """Get a single history record.

        This query returns the track, album, and artist data.
        """
        qs = super().prefetch_related("track", "track__album", "album__artists")

        return qs.get(pk=pk)

    def create_artist(self, artist: ListeningHistorySerializer.NestedArtist) -> Artist:
        """Create an artist."""
        obj, _ = Artist.objects.update_or_create(
            spotify_id=artist.spotify_id,
            defaults={"name": artist.name},
        )

        return obj

    def create_album(self, album: ListeningHistorySerializer.NestedAlbum) -> Album:
        """Create an album."""
        obj, _ = Album.objects.update_or_create(
            spotify_id=album.spotify_id,
            defaults={
                "name": album.name,
                "image_url": album.image_url,
                "release_year": album.release_date,
            },
        )

        return obj

    def create_track(self, track: ListeningHistorySerializer.NestedTrack) -> Track:
        """Create a track."""
        obj, _ = Track.objects.update_or_create(
            spotify_id=track.spotify_id,
            defaults={
                "name": track.name,
                "duration": track.duration,
            },
        )

        return obj

    def build(
        self, serialized: "ListeningHistorySerializer", user_pk: int, *args, **kwargs
    ) -> "ListeningHistory":
        """Create a history record.

        Also creates the track, album, and artist records if they don't exist.
        """
        track = self.create_track(serialized.track)
        history_item, _ = self.model.objects.get_or_create(
            user_id=user_pk,
            track=track,
            played_at=datetime.datetime.strptime(
                serialized.played_at, "%Y-%m-%dT%H:%M:%S.%fZ"
            ).replace(tzinfo=pytz.UTC),
        )

        album = self.create_album(serialized.album)
        for artist_obj in serialized.artists:
            artist = self.create_artist(artist_obj)
            album.artists.add(artist)
            artist.save()

        album.tracks.add(history_item.track)
        album.save()

        return history_item


class ListeningHistory(models.Model):
    """Last played."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    played_at = models.DateTimeField(null=False, blank=False)
    logged_at = models.DateTimeField(auto_now_add=True)

    track = models.ForeignKey("api.Track", on_delete=models.CASCADE)
    user = models.ForeignKey("core.AppUser", on_delete=models.CASCADE)

    objects = models.Manager()
    history = ListeningHistoryManager()

    class Meta(TypedModelMeta):
        """Model meta."""

        ordering = ["-played_at"]
        unique_together = ["played_at", "track"]
