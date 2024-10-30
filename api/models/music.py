"""Music Persistence Models.

Parking Lot
- (TODO) Musicbrainz integration models
"""

from django.db import models

from api.models.mixins import (
    CanBeAnalyzedMixin,
    CanBeSyncedMixin,
    SpotifyModel,
    TimestampedModel,
)


class Library(TimestampedModel):
    """Library metadata model."""

    user = models.OneToOneField(
        "core.AppUser", on_delete=models.CASCADE, related_name="library"
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
