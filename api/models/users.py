"""Custom user model.

Parking Lot:
- The password field is likely unecessary.
"""

import logging
import uuid

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django_stubs_ext.db.models import TypedModelMeta

from api.models.mixins import TokenSetMixin
from api.serializers.authentication import AccessToken, CurrentUser

logger = logging.getLogger(__name__)


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


class AppUser(TokenSetMixin, AbstractUser):
    """Application User Model (Custom)."""

    public_id = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    email = models.EmailField(blank=False, unique=True)

    username: None = None  # type: ignore
    first_name: None = None  # type: ignore
    last_name: None = None  # type: ignore

    spotify_id = models.CharField(max_length=255, unique=True)
    spotify_display_name = models.CharField(max_length=255, blank=True, unique=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: AppUserManager = AppUserManager()  # type: ignore

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
