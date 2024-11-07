from django.apps import AppConfig


class LiveConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "live"

    def ready(self) -> None:
        """Ensure signals are connected when the app is ready."""
        from live import signals  # noqa: F401
