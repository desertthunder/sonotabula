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


class SpotifyModel(models.Model):
    """Base model for Spotify API models."""

    public_id = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    spotify_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=False)

    class Meta(TypedModelMeta):
        """Meta options."""

        abstract = True


class Library(models.Model):
    """Library metadata model."""

    public_id = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    user_id: models.ForeignKey["AppUser", "Library"] = models.ForeignKey(
        "AppUser", related_name="libraries", on_delete=models.CASCADE
    )

    playlist_ids = models.ManyToManyField("api.Playlist", related_name="libraries")

    artist_ids = models.ManyToManyField("api.Artist", related_name="libraries")

    album_ids = models.ManyToManyField("api.Album", related_name="libraries")

    track_ids = models.ManyToManyField("api.Track", related_name="libraries")


class Playlist(SpotifyModel):
    """Spotify playlist model.

    Required fields for creation:
        - name
        - spotify_id
        - owner_id
    """

    user_id = models.ForeignKey(
        "api.AppUser", related_name="playlists", on_delete=models.PROTECT, null=True
    )
    owner_id = models.CharField(max_length=255, null=False)
    description = models.TextField(blank=True)
    track_ids = models.ManyToManyField("api.Track", related_name="playlists")


class Track(SpotifyModel):
    """Track model.

    Required fields for creation:
        - name
        - spotify_id
    """

    features = models.JSONField(default=dict)
    duration = models.IntegerField()
    playlist_ids = models.ManyToManyField(Playlist, related_name="tracks")


class Album(SpotifyModel):
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


class Artist(SpotifyModel):
    """Artist model.

    Required fields for creation:
        - name
        - spotify_id
    """

    image_url = models.URLField(blank=True)
    spotify_follower_count = models.IntegerField(blank=True)

    album_ids = models.ManyToManyField(Album, related_name="artists")
    genre_ids = models.ManyToManyField("api.Genre", related_name="artists")


class Genre(models.Model):
    """Genre model.

    Required fields for creation:
        - name
    """

    public_id = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255, unique=True)

    artist_ids = models.ManyToManyField(Artist, related_name="genres")
    album_ids = models.ManyToManyField(Album, related_name="genres")
