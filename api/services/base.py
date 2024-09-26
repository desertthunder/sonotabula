"""Spotify Service."""

import abc

import httpx
from django.db import models
from django_stubs_ext.db.models import TypedModelMeta

from server import settings


class TokenSetMixin(models.Model):
    """Token attributes."""

    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    token_expiry = models.DateTimeField()

    class Meta(TypedModelMeta):
        """TokenSet meta class."""

        abstract = True


class Services(models.TextChoices):
    """Service names enumeration."""

    spotify = "Spotify"
    musicbrainz = "Musicbrainz"


class SpotifyManager(models.Manager["Service"]):
    """Spotify Service Manager."""

    base_url: str = settings.SPOTIFY_BASE_URL
    _client: httpx.Client = None

    def set_client(self) -> httpx.Client:
        """Create HTTP client."""
        client = httpx.Client(base_url=self.base_url)

        return client

    @property
    def client(self) -> httpx.Client:
        """Client accessor."""
        if not self._client or self._client.is_closed:
            return self.set_client()

        return self._client

    def create(self, **kwargs: abc.Any) -> "Service":
        """Create an instance of the Spotify Service."""
        if not settings.SPOTIFY_CLIENT_ID or not settings.SPOTIFY_CLIENT_SECRET:
            raise ValueError("No credentials found")

        srv, _ = Service.objects.get_or_create(
            name=Services.spotify,
            client_id=settings.SPOTIFY_CLIENT_ID,
            client_secret=settings.SPOTIFY_CLIENT_SECRET,
        )

        return srv

    def authenticate(self, srv: "Service") -> str:
        """Authenticate the application using the available credentials.

        Returns:
            str Access Token returned from API call
        """
        pass


class MusicBrainzManager(models.Manager["Service"]):
    """MusicBrainz Manager."""

    pass


class Service(models.Model, TokenSetMixin):
    """3rd Party API Service."""

    client_id = models.CharField(unique=True)
    name = models.CharField(choices=Services, unique=True)

    spotify = SpotifyManager()
    musicbrainz = MusicBrainzManager()

    class Meta(TypedModelMeta):
        """Service base class meta."""

        abstract = True
