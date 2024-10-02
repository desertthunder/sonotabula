"""API Service models."""

import typing

import httpx
from django.db import models
from django_stubs_ext.db.models import TypedModelMeta

from api.models.mixins import TokenSetMixin
from server import settings


class Services(models.TextChoices):
    """Service names enumeration."""

    spotify = "Spotify"
    musicbrainz = "Musicbrainz"


class SpotifyManager(models.Manager["Service"]):
    """Spotify Service Manager."""

    base_url: str = settings.SPOTIFY_BASE_URL
    _client: httpx.Client

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

    def create(self, **kwargs: typing.Any) -> "Service":  # noqa: ANN401
        """Create an instance of the Spotify Service."""
        if not settings.SPOTIFY_CLIENT_ID or not settings.SPOTIFY_CLIENT_SECRET:
            raise ValueError("No credentials found")

        srv, _ = Service.objects.get_or_create(
            name=Services.spotify,
            client_id=settings.SPOTIFY_CLIENT_ID,
            client_secret=settings.SPOTIFY_CLIENT_SECRET,
        )

        return srv

    def request_user_authorization(self) -> None:
        """Request user authorization."""
        pass

    def request_access_token(self, authorization_code: str) -> None:
        """Request access token."""
        pass

    def get_user_profile(self, access_token: str) -> None:
        """Get user profile."""
        pass

    def create_user_from_spotify_profile(
        self,
        user_data: dict,
        access_token: str,
        refresh_token: str,
        expiry: int = 3600,
    ) -> None:
        """Create user."""
        pass

    def refresh_access_token(self, refresh_token: str) -> None:
        """Refresh access token."""
        pass


class MusicBrainzManager(models.Manager["Service"]):
    """MusicBrainz Manager."""

    pass


class Service(TokenSetMixin, models.Model):
    """3rd Party API Service."""

    client_id = models.CharField(unique=True)
    name = models.CharField(choices=Services, unique=True)

    objects: models.Manager["Service"]
    spotify = SpotifyManager()
    musicbrainz = MusicBrainzManager()

    class Meta(TypedModelMeta):
        """Meta class for Service."""

        pass
