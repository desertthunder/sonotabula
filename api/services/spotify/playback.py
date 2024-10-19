"""Playback Spotify API Service class.

Parking Lot:
- TODO: Now playing
"""

import json
import logging
import typing

import httpx

from api.libs.constants import SpotifyAPIEndpoints
from api.libs.exceptions import SpotifyAPIError, SpotifyExpiredTokenError
from api.models import AppUser
from api.services.spotify.auth import SpotifyAuthService

logger = logging.getLogger("spotify_playback_service")
auth_service = SpotifyAuthService()


class SpotifyPlaybackService:
    """API actions for fetching data from the Spotify API."""

    def __init__(self, auth: SpotifyAuthService = auth_service) -> None:
        """Initialize the service."""
        self.auth_service = auth

    def get_user(self, user_pk: int) -> "AppUser":
        """Get a user by primary key."""
        return AppUser.objects.get(pk=user_pk)

    def handle_error(self, response: httpx.Response) -> None:
        """Handle Spotify API errors."""
        logger.error(f"Error: {response.text}")

        error = json.loads(response.text).get("error")

        if (
            error.get("status") == 401
            and error.get("message") == "The access token expired"
        ):
            raise SpotifyExpiredTokenError("The access token expired")

        raise SpotifyAPIError(response.text)

    def recently_played(
        self, user_pk: int, items: int = 10, all: bool = False
    ) -> typing.Iterable[dict]:
        """Get the user's recently played track."""
        try:
            user = self.get_user(user_pk)
            yield from self._recently_played(user, items, all)
        except AppUser.DoesNotExist:
            logger.error(f"User {user_pk} does not exist.")
            yield from []
        except SpotifyExpiredTokenError:
            logger.error(f"User {user_pk} has an expired token.")
            self.auth_service.refresh_access_token(user.refresh_token)
            user.refresh_from_db()

            yield from self._recently_played(user, items, all)

    def now_playing(self) -> dict:
        """Get the user's currently playing track."""
        raise NotImplementedError

    def _recently_played(
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
                    self.handle_error(response)

                resp = response.json()

                logger.debug(f"Response: {resp}")

                next = resp.get("next")

                if next is not None:
                    next = next.replace(f"{SpotifyAPIEndpoints.BASE_URL}/", "")

                if not all:
                    yielded += len(resp.get("items"))

                yield from resp.get("items")
