"""Playback Spotify API Service class.

Parking Lot:
- TODO: Now playing
"""

import logging
import typing

import httpx

from api.libs.constants import SpotifyAPIEndpoints
from api.libs.exceptions import SpotifyAPIError

if typing.TYPE_CHECKING:
    from api.models import AppUser

logger = logging.getLogger("spotify_playback_service")


class SpotifyPlaybackService:
    """API actions for fetching data from the Spotify API."""

    def now_playing(self) -> dict:
        """Get the user's currently playing track."""
        raise NotImplementedError

    def recently_played(
        self, user: "AppUser", items: int = 10, all: bool = False
    ) -> typing.Iterable[dict]:
        """Get the user's recently played track."""
        yielded = 0
        next = f"{SpotifyAPIEndpoints.RecentlyPlayed}"

        with httpx.Client(base_url=SpotifyAPIEndpoints.BASE_URL) as client:
            while next:
                if not all and yielded >= items:
                    break

                response = client.get(
                    url=SpotifyAPIEndpoints.RecentlyPlayed,
                    headers={"Authorization": f"Bearer {user.access_token}"},
                    params={"limit": items},
                )

                if response.is_error:
                    error = response.json().get("error")

                    logger.error(f"{error.get("status")} Error: {error.get("message")}")

                    raise SpotifyAPIError(response.text)

                resp = response.json()

                logger.debug(f"Response: {resp}")

                next = resp.get("next")

                if next is not None:
                    next = next.replace(f"{SpotifyAPIEndpoints.BASE_URL}/", "")

                if not all:
                    yielded += len(resp.get("items"))

                yield from resp.get("items")
