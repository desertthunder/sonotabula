"""Music Persistence Models.

Parking Lot
- Musicbrainz integration
"""

import typing
import uuid

from django.db import models
from django_stubs_ext.db.models import TypedModelMeta

from api.models.mixins import CanBeAnalyzedMixin, CanBeSyncedMixin

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

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    spotify_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=False)

    class Meta(TypedModelMeta):
        """Meta options."""

        abstract = True


class Library(TimestampedModel):
    """Library metadata model."""

    user: models.ForeignKey["AppUser", "Library"] = models.ForeignKey(
        "AppUser", related_name="libraries", on_delete=models.CASCADE
    )

    artists = models.ManyToManyField("api.Artist", related_name="libraries")
    tracks = models.ManyToManyField("api.Track", related_name="libraries")


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
    libraries = models.ManyToManyField(Library, related_name="albums")
    genres = models.ManyToManyField("api.Genre", related_name="albums")


class Artist(SpotifyModel, TimestampedModel, CanBeSyncedMixin):
    """Artist model.

    Required fields for creation:
        - name
        - spotify_id
    """

    image_url = models.URLField(blank=True, null=True)
    spotify_follower_count = models.IntegerField(blank=True, null=True)
    albums = models.ManyToManyField(Album, related_name="artists")
    genres = models.ManyToManyField("api.Genre", related_name="artists")


class Genre(TimestampedModel):
    """Genre model.

    Required fields for creation:
        - name
    """

    name = models.CharField(max_length=255, unique=True, null=False, blank=False)
