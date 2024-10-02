"""Setup/Bootstrap Third-Party API Providers."""

import typing
from dataclasses import dataclass

from loguru import logger

from api.models.services import SpotifyManager


@dataclass
class _Services:
    """Service type."""

    spotify: tuple[str, SpotifyManager] = ("spotify", SpotifyManager())


class Setup:
    """Callable class to setup third-party API services."""

    services: _Services

    def __init__(
        self,
        *args: typing.Unpack[tuple],
        **kwargs: typing.Unpack[dict],  # type: ignore[misc]
    ) -> None:
        """Initialize the class."""
        self.services = _Services()

    def __call__(self) -> None:
        """Setup the services."""
        name, manager = self.services.spotify

        logger.debug(f"Setting up {name} service")

        s = manager.create()

        logger.info(f"{name} service setup complete with pk: {s.pk}")

        return
