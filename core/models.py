"""Custom user model.

Parking Lot:
- The password field is likely unecessary.
"""

import datetime
import typing

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils import timezone
from django_stubs_ext.db.models import TypedModelMeta
from loguru import logger
from pydantic import BaseModel

from api.models.mixins import TimestampedModel, TokenSetMixin


class Serializer(BaseModel):
    """Base class for serializing data."""

    @classmethod
    def mappings(cls: type[typing.Self]) -> dict[str, str]:
        """Mapping of JSON data to class properties."""
        raise NotImplementedError("Subclasses must implement this method.")

    @classmethod
    def nullable_fields(cls: type[typing.Self]) -> tuple:
        """Fields that can be null."""
        raise NotImplementedError("Subclasses must implement this method.")

    @classmethod
    def map_response(cls: type[typing.Self], response: dict) -> dict:
        """Map JSON data to class properties."""
        data = {}

        for key, value in cls.mappings().items():
            path = value.split(".")
            prop = response.copy()

            for p in path:
                if p.isdigit() and isinstance(prop, list):
                    i = int(p)
                    prop = prop[i]
                elif isinstance(prop, dict) and prop.get(p):
                    prop = prop.get(p)  # type: ignore
            if isinstance(prop, dict):
                prop = ""  # type: ignore

            if prop is not None:
                data[key] = prop

        for field in cls.nullable_fields():
            data[field] = response.get(field)  # type: ignore
        return data

    @classmethod
    def get(cls: type[typing.Self], response: dict) -> typing.Self:
        """Create a Serializer object from JSON data."""
        data: dict = cls.map_response(response)

        return cls(**data)

    @classmethod
    def list(
        cls: type[typing.Self], response: list[dict]
    ) -> typing.Iterable[typing.Self]:
        """Create a list of Serializer objects from JSON data."""
        for item in response:
            yield cls.get(item)


class AccessToken(Serializer):
    """Spotify Access Token Response Data."""

    access_token: str
    refresh_token: str
    token_type: str
    token_expiry: datetime.datetime

    @classmethod
    def mappings(cls: type["AccessToken"]) -> dict:
        """Mapping of JSON data to class properties."""
        return {
            "access_token": "access_token",
            "refresh_token": "refresh_token",
            "token_type": "token_type",
        }

    @classmethod
    def nullable_fields(cls: type["AccessToken"]) -> tuple[str]:
        """Fields that can be null."""
        return ("token_expiry",)

    @classmethod
    def get(cls: type["AccessToken"], response: dict) -> "AccessToken":
        """Create a Serializer object from JSON data."""
        data: dict = cls.map_response(response)

        if "token_expiry" in data and data.get("token_expiry"):
            token_expiry = int(data["token_expiry"])
            data["token_expiry"] = timezone.now() + datetime.timedelta(
                seconds=token_expiry
            )
        elif "expires_in" in response and response.get("expires_in"):
            token_expiry = int(response["expires_in"])
            data["token_expiry"] = timezone.now() + datetime.timedelta(
                seconds=token_expiry
            )
        return cls(**data)


class SpotifyUserSerializer(Serializer):
    """Spotify Current User Data."""

    id: str
    email: str
    display_name: str

    @classmethod
    def mappings(cls: type["SpotifyUserSerializer"]) -> dict:
        """Mapping of JSON data to class properties."""
        return {
            "display_name": "display_name",
            "email": "email",
            "id": "id",
        }

    @classmethod
    def nullable_fields(cls: type["SpotifyUserSerializer"]) -> tuple[str]:
        """Fields that can be null."""
        return ("",)


class AppUserManager(UserManager["AppUser"]):
    """Application User Manager."""

    def from_spotify(self, data: dict, token_data: dict) -> "AppUser":
        """Find or Create a user from spotify data."""
        try:
            spotify_data = SpotifyUserSerializer.get(data)
            tokens = AccessToken.get(token_data)

            user = self.get(spotify_id=spotify_data.id)

            logger.debug(f"Found user: {user.public_id}")

            user.update_token_set(tokens)
        except AppUser.DoesNotExist:
            user = self.create(
                spotify_id=spotify_data.id,
                email=spotify_data.email,
                spotify_display_name=spotify_data.display_name,
                access_token=tokens.access_token,
                refresh_token=tokens.refresh_token,
                token_expiry=tokens.token_expiry,
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
