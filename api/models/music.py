"""Music Persistence Models.

Parking Lot
- Musicbrainz integration
"""

import typing
import uuid

from django.db import models
from django_stubs_ext.db.models import TypedModelMeta

if typing.TYPE_CHECKING:
    from api.models.users import AppUser


class TimestampedModel(models.Model):
    """Base model for timestamped models."""

    public_id = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta options."""

        abstract = True


class SpotifyModel(models.Model):
    """Base model for Spotify API models."""

    spotify_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=False)

    class Meta(TypedModelMeta):
        """Meta options."""

        abstract = True


class Library(TimestampedModel):
    """Library metadata model."""

    user_id: models.ForeignKey["AppUser", "Library"] = models.ForeignKey(
        "AppUser", related_name="libraries", on_delete=models.CASCADE
    )

    playlist_ids = models.ManyToManyField("api.Playlist", related_name="libraries")

    artist_ids = models.ManyToManyField("api.Artist", related_name="libraries")

    album_ids = models.ManyToManyField("api.Album", related_name="libraries")

    track_ids = models.ManyToManyField("api.Track", related_name="libraries")


class Playlist(SpotifyModel, TimestampedModel):
    """Spotify playlist model.

    Required fields for creation:
        - name
        - spotify_id
        - owner_id
    """

    version = models.CharField(max_length=255, blank=True)  # snapshot_id
    image_url = models.URLField(blank=True)
    public = models.BooleanField(null=True)
    shared = models.BooleanField(null=True)  # collaborative
    description = models.TextField(blank=True, null=True)

    user_id = models.ForeignKey(
        "api.AppUser", related_name="playlists", on_delete=models.PROTECT, null=True
    )
    owner_id = models.CharField(max_length=255, null=False)
    track_ids = models.ManyToManyField("api.Track", related_name="playlists")


class Track(SpotifyModel, TimestampedModel):
    """Track model.

    Required fields for creation:
        - name
        - spotify_id
    """

    duration = models.IntegerField()
    playlist_ids = models.ManyToManyField(Playlist, related_name="tracks")
    album_id = models.ForeignKey(
        "api.Album", related_name="tracks", on_delete=models.PROTECT, null=True
    )


class Album(SpotifyModel, TimestampedModel):
    """Album model.

    Required fields for creation:
        - name
        - spotify_id
    """

    album_type = models.CharField(max_length=255, blank=True)
    image_url = models.URLField(blank=True)
    label = models.CharField(max_length=255, blank=True)
    copyright = models.CharField(max_length=255, blank=True)
    release_year = models.IntegerField()

    artist_ids = models.ManyToManyField("api.Artist", related_name="albums")
    genre_ids = models.ManyToManyField("api.Genre", related_name="albums")


class Artist(SpotifyModel, TimestampedModel):
    """Artist model.

    Required fields for creation:
        - name
        - spotify_id
    """

    image_url = models.URLField(blank=True)
    spotify_follower_count = models.IntegerField(blank=True)

    album_ids = models.ManyToManyField(Album, related_name="artists")
    genre_ids = models.ManyToManyField("api.Genre", related_name="artists")


class Genre(TimestampedModel):
    """Genre model.

    Required fields for creation:
        - name
    """

    name = models.CharField(max_length=255, unique=True)

    artist_ids = models.ManyToManyField(Artist, related_name="genres")
    album_ids = models.ManyToManyField(Album, related_name="genres")
