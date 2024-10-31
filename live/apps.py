"""Live app configuration."""

from django.apps import AppConfig


class LiveConfig(AppConfig):
    """Live app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "live"
