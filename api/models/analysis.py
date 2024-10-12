"""Analysis models."""

from django.db import models

from api.models.music import TimestampedModel
from api.models.playlist import Playlist
from api.models.track import Track


class TrackFeatures(TimestampedModel):
    """Track feature record.

    One-to-one relationship with Track model.
    """

    track = models.OneToOneField(
        Track, on_delete=models.CASCADE, related_name="features"
    )

    danceability = models.FloatField()
    energy = models.FloatField()
    key = models.IntegerField()
    loudness = models.FloatField()
    mode = models.IntegerField()
    speechiness = models.FloatField()
    acousticness = models.FloatField()
    instrumentalness = models.FloatField()
    liveness = models.FloatField()
    valence = models.FloatField()
    tempo = models.FloatField()
    duration_ms = models.IntegerField()
    time_signature = models.IntegerField()


class Analysis(TimestampedModel):
    """Analysis model.

    Constructed from a single playlist (one-to-one relationship).

    Has many tracks.

    Represents a snapshot of the playlist at a given time,
    with associated tracks.
    """

    version = models.CharField(max_length=255, unique=True, null=False)
    playlist = models.OneToOneField(
        Playlist, on_delete=models.CASCADE, related_name="analysis"
    )
    user = models.ForeignKey("api.AppUser", on_delete=models.CASCADE)
    tracks = models.ManyToManyField(Track, related_name="analyses")
