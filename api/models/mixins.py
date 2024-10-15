"""API Model Mixins."""

import uuid

from django.db import models
from django_stubs_ext.db.models import TypedModelMeta


class TokenSetMixin(models.Model):
    """Token attributes."""

    access_token = models.CharField()
    refresh_token = models.CharField()
    token_expiry = models.DateTimeField()

    @property
    def token_expired(self) -> bool:
        """Check if the token is expired."""
        return True

    class Meta(TypedModelMeta):
        """TokenSet meta class."""

        abstract = True


class CanBeSyncedMixin(models.Model):
    """Sync attributes."""

    is_synced = models.BooleanField(default=False, null=True, blank=True)

    class Meta(TypedModelMeta):
        """CanBeSynced meta class."""

        abstract = True


class CanBeAnalyzedMixin(CanBeSyncedMixin):
    """Analyze attributes."""

    is_analyzed = models.BooleanField(default=False, null=True, blank=True)

    class Meta(TypedModelMeta):
        """CanBeAnalyzed meta class."""

        abstract = True


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
