"""API SQL Models."""

import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django_stubs_ext.db.models import TypedModelMeta

from api.services.base import (
    Service,  # noqa: F401
    TokenSetMixin,
)


class AppUser(AbstractUser, TokenSetMixin):
    """Application User Model (Custom)."""

    public_id = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    email = models.EmailField(blank=False, unique=True)

    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta(TypedModelMeta):
        """Meta class for app user."""
