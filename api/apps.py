"""API app configuration module."""

from django.apps import AppConfig


class ApiConfig(AppConfig):
    """API app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "api"
