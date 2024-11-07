"""Custom user model.

Parking Lot:
- The password field is likely unecessary.
"""

import datetime

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils import timezone
from django_stubs_ext.db.models import TypedModelMeta
from loguru import logger

from api.models.mixins import TimestampedModel, TokenSetMixin
from api.serializers.authentication import AccessToken, CurrentUser


class AppUserManager(UserManager["AppUser"]):
    """Application User Manager."""

    def from_spotify(
        self,
        spotify_data: CurrentUser,
        token_set: AccessToken,
    ) -> "AppUser":
        """Find or Create a user from spotify data."""
        try:
            user = self.get(spotify_id=spotify_data.id)

            logger.debug(f"Found user: {user.public_id}")

            user.update_token_set(token_set)
        except AppUser.DoesNotExist:
            user = self.create(
                spotify_id=spotify_data.id,
                email=spotify_data.email,
                spotify_display_name=spotify_data.display_name,
                access_token=token_set.access_token,
                refresh_token=token_set.refresh_token,
                token_expiry=token_set.token_expiry,
            )

            user.save()
            user.refresh_from_db()

            logger.debug(f"Created user: {user.public_id}")

        return user


class AppUser(TokenSetMixin, TimestampedModel, AbstractUser):
    """Application User Model (Custom)."""

    email = models.EmailField(blank=False, unique=True)

    image_url = models.URLField(blank=True, max_length=512)
    saved_tracks = models.IntegerField(default=0)
    saved_albums = models.IntegerField(default=0)
    saved_playlists = models.IntegerField(default=0)
    saved_artists = models.IntegerField(default=0)
    saved_shows = models.IntegerField(default=0)

    username: None = None  # type: ignore
    first_name: None = None  # type: ignore
    last_name: None = None  # type: ignore

    spotify_id = models.CharField(max_length=255, unique=True)
    spotify_display_name = models.CharField(max_length=255, blank=True, unique=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: AppUserManager = AppUserManager()  # type: ignore

    @property
    def should_update(self) -> bool:
        """Check if the user should refresh their counts."""
        no_counts = (
            self.saved_tracks == 0
            or self.saved_albums == 0
            or self.saved_playlists == 0
            or self.saved_artists == 0
            or self.saved_playlists == 0
            or self.saved_shows == 0
        )

        stale = timezone.now() - self.updated_at > datetime.timedelta(hours=6)

        return no_counts or stale

    def update_token_set(self, token_set: AccessToken) -> "AppUser":
        """Update the user's token set."""
        self.access_token = token_set.access_token
        self.refresh_token = token_set.refresh_token
        self.token_expiry = token_set.token_expiry

        logger.debug(f"Updated token set for user: {self.public_id}")

        self.save(update_fields=["access_token", "refresh_token", "token_expiry"])
        self.refresh_from_db()

        return self

    class Meta(TypedModelMeta):
        """Meta class for app user."""

        pass
