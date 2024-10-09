"""Spotify data service."""

import logging
import typing

import httpx

from api.libs.constants import SpotifyAPIEndpoints
from api.libs.exceptions import SpotifyAPIError

if typing.TYPE_CHECKING:
    from api.models import AppUser

logger = logging.getLogger("spotify_data_service")


class SpotifyDataService:
    """API actions for fetching data from the Spotify API."""

    def now_playing(self) -> None:
        """Get the user's currently playing track."""
        pass

    def recently_played(self, user: "AppUser", items: int = 10) -> list[dict]:
        """Get the user's last played track."""
        with httpx.Client(base_url=SpotifyAPIEndpoints.BASE_URL) as client:
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

            client.close()

        tracks = resp.get("items") or []

        return tracks

    def last_played(self, user: "AppUser") -> list[dict]:
        """Get the user's last played track."""
        return self.recently_played(user, 1)

    def library_playlists(self, user: "AppUser", limit: int = 50) -> list[dict]:
        """Get the user's playlists."""
        with httpx.Client(
            base_url=SpotifyAPIEndpoints.BASE_URL,
            headers={"Authorization": f"Bearer {user.access_token}"},
        ) as client:
            response = client.get(
                url=SpotifyAPIEndpoints.SavedPlaylists,
                params={"limit": limit},
            )

            if response.is_error:
                logger.error(f"Error: {response.text}")

                raise SpotifyAPIError(response.text)

            resp = response.json()

            logger.debug(f"Response: {resp}")

            client.close()

        playlists = resp.get("items") or []

        return playlists

    def library_albums(self, user: "AppUser", limit: int = 50) -> list[dict]:
        """Get the user's albums."""
        with httpx.Client(
            base_url=SpotifyAPIEndpoints.BASE_URL,
            headers={"Authorization": f"Bearer {user.access_token}"},
        ) as client:
            response = client.get(
                url=SpotifyAPIEndpoints.SavedAlbums,
                params={"limit": limit},
            )

            if response.is_error:
                logger.error(f"Error: {response.text}")

                raise SpotifyAPIError(response.text)

            resp = response.json()

            logger.debug(f"Response: {resp}")

            client.close()

        albums = resp.get("items") or []

        return albums

    def library_artists(self, user: "AppUser", limit: int = 50) -> list[dict]:
        """Get the user's followed artists."""
        with httpx.Client(
            base_url=SpotifyAPIEndpoints.BASE_URL,
            headers={"Authorization": f"Bearer {user.access_token}"},
        ) as client:
            response = client.get(
                url=SpotifyAPIEndpoints.FollowedArtists,
                params={"type": "artist", "limit": limit},
            )

            if response.is_error:
                logger.error(f"Error: {response.text}")

                raise SpotifyAPIError(response.text)

            resp = response.json()

            logger.debug(f"Response: {resp}")

            client.close()

        artists = resp.get("artists", {}).get("items") or []

        return artists

    def library_tracks(self, user: "AppUser", limit: int = 50) -> list[dict]:
        """Get the user's saved tracks."""
        with httpx.Client(
            base_url=SpotifyAPIEndpoints.BASE_URL,
            headers={"Authorization": f"Bearer {user.access_token}"},
        ) as client:
            response = client.get(
                url=SpotifyAPIEndpoints.SavedTracks,
                params={"limit": limit},
            )

            if response.is_error:
                logger.error(f"Error: {response.text}")

                raise SpotifyAPIError(response.text)

            resp = response.json()

            logger.debug(f"Response: {resp}")

            client.close()

        tracks = resp.get("items") or []

        return tracks

    def top_tracks(self) -> None:
        """Get the user's top tracks."""
        pass
