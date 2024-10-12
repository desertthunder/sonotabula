"""Spotify data service.

Fetches individual records.

Parking Lot:
- When an individual artist, album, or track is fetched,
    the data is stored in the database.
- Artist and album fetching should include related artists and albums.
    - The endpoint should dispatch a task.
"""

import logging
import time
import typing

import httpx

from api.libs.constants import SpotifyAPIEndpoints
from api.libs.exceptions import SpotifyAPIError, SpotifyExpiredTokenError
from api.models.users import AppUser
from api.services.spotify.auth import SpotifyAuthService

logger = logging.getLogger(__name__)


class SpotifyDataService:
    """Single record data service."""

    def get_user(self, user_pk: int) -> "AppUser":
        """Get user data."""
        return AppUser.objects.get(pk=user_pk)

    def fetch_playlist_tracks(
        self, playlist_id: str, user_pk: int
    ) -> typing.Iterable[dict]:
        """Fetch playlist tracks."""
        user = self.get_user(user_pk)

        try:
            yield from self._fetch_playlist_tracks(playlist_id, user=user)
        except SpotifyExpiredTokenError:
            user_service = SpotifyAuthService()
            user_service.refresh_access_token(user.refresh_token)

            user.refresh_from_db()

            yield from self._fetch_playlist_tracks(playlist_id, user=user)

    def fetch_saved_items(
        self,
        user: "AppUser",
        limit: int = 5,
    ) -> typing.Iterable[tuple[str, dict]]:
        """Fetch saved items from Spotify API."""
        paths = [
            SpotifyAPIEndpoints.SavedTracks,
            SpotifyAPIEndpoints.SavedAlbums,
            SpotifyAPIEndpoints.SavedPlaylists,
            SpotifyAPIEndpoints.SavedShows,
            SpotifyAPIEndpoints.FollowedArtists,
        ]

        with httpx.Client(
            base_url=SpotifyAPIEndpoints.BASE_URL,
            headers={"Authorization": f"Bearer {user.access_token}"},
        ) as client:
            for path in paths:
                params = {"limit": str(limit)}

                if path == SpotifyAPIEndpoints.FollowedArtists:
                    params["type"] = "artist"

                response = client.get(url=path, params=params)

                if response.is_error:
                    logger.error(f"Error: {response.text}")

                    raise SpotifyAPIError(response.text)

                resp = response.json()

                logger.debug(f"Response: {resp}")

                if path == SpotifyAPIEndpoints.FollowedArtists:
                    yield (path, resp.get("artists", {}))
                else:
                    yield (path, resp)

    def fetch_playlist(self, playlist_id: str, user: "AppUser") -> dict:
        """Fetch playlist data from Spotify API."""
        with httpx.Client(
            base_url=SpotifyAPIEndpoints.BASE_URL,
            headers={"Authorization": f"Bearer {user.access_token}"},
        ) as client:
            response = client.get(
                url=SpotifyAPIEndpoints.Playlist.format(playlist_id=playlist_id)
            )

            if response.is_error:
                logger.error(f"Error: {response.text}")

                raise SpotifyAPIError(response.text)

            resp = response.json()

            logger.debug(f"Response: {resp}")

            client.close()

            return resp

    def _fetch_playlist_tracks(
        self, playlist_id: str, user: "AppUser"
    ) -> typing.Iterable[dict]:
        """Fetch a playlist's tracks."""
        next = SpotifyAPIEndpoints.PlaylistTracks.format(playlist_id=playlist_id)

        with httpx.Client(
            base_url=SpotifyAPIEndpoints.BASE_URL,
            headers={"Authorization": f"Bearer {user.access_token}"},
        ) as client:
            while next:
                response = client.get(url=next)

                if response.is_error:
                    logger.error(f"Error: {response.text}")

                    raise SpotifyAPIError(response.text)

                resp = response.json()

                logger.debug(f"No. Tracks: {len(resp.get("items", []))} items")
                logger.debug(f"Next: {resp.get('next')}")

                next = resp.get("next")

                if next:
                    next = next.replace(f"{SpotifyAPIEndpoints.BASE_URL}/", "")

                yield from resp.get("items", [])

    def fetch_audio_features(
        self, track_ids: list[str], user_pk: int
    ) -> typing.Iterable[dict]:
        """Fetch audio features."""
        user = self.get_user(user_pk)

        try:
            yield from self._fetch_audio_features(track_ids, user)
        except SpotifyExpiredTokenError:
            user_service = SpotifyAuthService()
            user_service.refresh_access_token(user.refresh_token)

            user.refresh_from_db()

            yield from self._fetch_audio_features(track_ids, user)

    def _fetch_audio_features(
        self, track_ids: list[str], user: "AppUser"
    ) -> typing.Iterable[dict]:
        """Fetch audio features."""
        batches = [track_ids[i : i + 50] for i in range(0, len(track_ids), 50)]

        with httpx.Client(
            base_url=SpotifyAPIEndpoints.BASE_URL,
            headers={"Authorization": f"Bearer {user.access_token}"},
        ) as client:
            for batch in batches:
                time.sleep(0.5)
                response = client.get(
                    url=SpotifyAPIEndpoints.BulkTrackAudioFeatures,
                    params={"ids": ",".join(batch)},
                )

                if response.is_error:
                    logger.error(f"Error: {response.text}")
                    logger.error(batch)
                    raise SpotifyAPIError(response.text)

                resp = response.json()

                logger.debug(f"Response: {resp}")

                time.sleep(0.5)

                yield from resp.get("audio_features", [])
