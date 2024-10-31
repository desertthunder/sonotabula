"""Browser app models."""

from django.db import models

from core.mixins import Model


# Create your models here.
class Library(Model):
    """Library metadata model."""

    user = models.OneToOneField(
        "core.AppUser", on_delete=models.CASCADE, related_name="library"
    )

    artists = models.ManyToManyField("api.Artist", related_name="libraries")
    tracks = models.ManyToManyField("api.Track", related_name="libraries")
    albums = models.ManyToManyField("api.Album", related_name="libraries")
    genres = models.ManyToManyField("api.Genre", related_name="libraries")
    playlists = models.ManyToManyField("api.Playlist", related_name="libraries")
