"""Spotify data service."""

import time
import typing

import httpx
from loguru import logger

from api.libs.constants import SpotifyAPIEndpoints
from api.libs.exceptions import SpotifyAPIError, SpotifyExpiredTokenError
from api.services.spotify.auth import SpotifyAuthService
from core.models import AppUser

logger.add("logs/spotify_data.log", rotation="1 MB", retention="1 day", level="DEBUG")


class SpotifyLibraryService:
    """API actions for fetching data from the Spotify API."""

    def __init__(self, auth_service: SpotifyAuthService | None = None) -> None:
        """Add dependencies to the service."""
        self.auth_service = auth_service or SpotifyAuthService()

    def get_user(self, user_pk: int) -> "AppUser":
        """Get a user by primary key."""
        return AppUser.objects.get(pk=user_pk)

    def handle_error(self, response: httpx.Response) -> None:
        """Handle Spotify API errors."""
        logger.error(f"Error: {response.text}")
        logger.error(f"Status: {response.status_code}")

        if response.text and response.json():
            error = response.json().get("error")
        else:
            error = {"status": response.status_code, "message": response.text}

        if (
            error.get("status") == 401
            and error.get("message") == "The access token expired"
        ):
            raise SpotifyExpiredTokenError("The access token expired")

        raise SpotifyAPIError(response.text)

    def library_playlists(
        self, user_pk: int, limit: int = 50, offset: int = 0, all: bool = False
    ) -> typing.Iterable[dict]:
        """Get the user's playlists.

        Refresh the access token if it has expired.
        """
        user = self.get_user(user_pk)

        try:
            yield from self._library_playlists(
                user=user, limit=limit, offset=offset, all=all
            )
        except SpotifyExpiredTokenError:
            self.auth_service.refresh_access_token(user.refresh_token)

            user.refresh_from_db()

            yield from self._library_playlists(user=user, limit=limit, all=all)

    def library_track(self, user_pk: int, track_id: str) -> dict:
        """Get the user's track."""
        user = self.get_user(user_pk)
        try:
            response = httpx.get(
                url=f"{SpotifyAPIEndpoints.BASE_URL}/{SpotifyAPIEndpoints.Track.format(track_id=track_id)}",
                headers={"Authorization": f"Bearer {user.access_token}"},
            )

            if response.is_error:
                self.handle_error(response)

            return response.json()
        except SpotifyExpiredTokenError:
            self.auth_service.refresh_access_token(user.refresh_token)

            user.refresh_from_db()

            response = httpx.get(
                url=f"{SpotifyAPIEndpoints.BASE_URL}/{SpotifyAPIEndpoints.Track.format(track_id=track_id)}",
                headers={"Authorization": f"Bearer {user.access_token}"},
            )

            if response.is_error:
                self.handle_error(response)

        return response.json()

    def library_playlists_total(self, user_pk: int) -> int:
        """Get the total number of playlists."""
        user = self.get_user(user_pk)

        response = httpx.get(
            url=f"{SpotifyAPIEndpoints.BASE_URL}/{SpotifyAPIEndpoints.SavedPlaylists}",
            headers={"Authorization": f"Bearer {user.access_token}"},
            params={"limit": 1},
        )

        if response.is_error:
            self.handle_error(response)

        total = response.json().get("total", "0")

        time.sleep(0.5)

        return int(total)

    def library_albums(
        self, user_pk: int, limit: int = 50, offset: int = 0, all: bool = False
    ) -> typing.Iterable[dict]:
        """Get the user's albums.

        Refresh the access token if it has expired.
        """
        user = self.get_user(user_pk)

        try:
            yield from self._library_albums(
                user=user, limit=limit, offset=offset, all=all
            )
        except SpotifyExpiredTokenError:
            self.auth_service.refresh_access_token(user.refresh_token)

            user.refresh_from_db()

            yield from self._library_albums(user=user, limit=limit, all=all)
        except Exception as e:
            logger.error("Request to get albums failed.")
            logger.error(f"Error: {e}")

            raise SpotifyAPIError(str(e)) from e

    def library_artists(
        self, user_pk: int, limit: int = 50, all: bool = False, last: str | None = None
    ) -> typing.Iterable[dict]:
        """Get the user's followed artists.

        Refresh the access token if it has expired.
        """
        user = self.get_user(user_pk)

        try:
            yield from self._library_artists(user=user, limit=limit, last=last, all=all)
        except SpotifyExpiredTokenError:
            self.auth_service.refresh_access_token(user.refresh_token)

            user.refresh_from_db()

            yield from self._library_artists(user=user, limit=limit, all=all)

    def library_tracks(
        self, user_pk: int, limit: int = 50, offset: int = 0, all: bool = False
    ) -> typing.Iterable[dict]:
        """Get the user's saved tracks.

        Refresh the access token if it has expired.
        """
        user = self.get_user(user_pk)

        try:
            yield from self._library_tracks(
                user=user, limit=limit, offset=offset, all=all
            )
        except SpotifyExpiredTokenError:
            self.auth_service.refresh_access_token(user.refresh_token)

            user.refresh_from_db()

            yield from self._library_tracks(user=user, limit=limit, all=all)

    def library_tracks_total(self, user_pk: int) -> int:
        """Get the total number of saved tracks."""
        user = self.get_user(user_pk)

        response = httpx.get(
            url=f"{SpotifyAPIEndpoints.BASE_URL}/{SpotifyAPIEndpoints.SavedTracks}",
            headers={"Authorization": f"Bearer {user.access_token}"},
            params={"limit": 1},
        )

        if response.is_error:
            self.handle_error(response)

        total = response.json().get("total", "0")

        time.sleep(0.5)

        return int(total)

    def library_albums_total(self, user_pk: int) -> int:
        """Get the total number of saved albums."""
        user = self.get_user(user_pk)

        response = httpx.get(
            url=f"{SpotifyAPIEndpoints.BASE_URL}/{SpotifyAPIEndpoints.SavedAlbums}",
            headers={"Authorization": f"Bearer {user.access_token}"},
            params={"limit": 1},
        )

        if response.is_error:
            self.handle_error(response)

        total = response.json().get("total", "0")

        time.sleep(0.5)

        return int(total)

    def library_playlist(self, user_pk: int, playlist_id: str, *args, **kwargs) -> dict:
        """Get the user's playlist with items.

        Refresh the access token if it has expired.
        """
        user = self.get_user(user_pk)

        try:
            return self._library_playlist(user=user, playlist_id=playlist_id)
        except SpotifyExpiredTokenError:
            self.auth_service.refresh_access_token(user.refresh_token)

            user.refresh_from_db()

            return self._library_playlist(user=user, playlist_id=playlist_id)
        except Exception as e:
            logger.error(f"Request to get playlist {playlist_id} items failed.")
            logger.error(f"Error: {e}")

            raise SpotifyAPIError(str(e)) from e

    def library_artists_total(self, user_pk: int) -> int:
        """Get the total number of followed artists."""
        user = self.get_user(user_pk)

        response = httpx.get(
            url=f"{SpotifyAPIEndpoints.BASE_URL}/{SpotifyAPIEndpoints.FollowedArtists}",
            headers={"Authorization": f"Bearer {user.access_token}"},
            params={"limit": 1, "type": "artist"},
        )

        if response.is_error:
            self.handle_error(response)

        total = response.json().get("artists", {}).get("total", "0")

        time.sleep(0.5)

        return int(total)

    def _library_playlists(
        self, user: "AppUser", limit: int = 50, offset: int = 0, all: bool = False
    ) -> typing.Iterable[dict]:
        yielded = 0
        next: str | None = f"{SpotifyAPIEndpoints.SavedPlaylists}"

        if all:
            limit = 50  # Default page size is 20

        with httpx.Client(
            base_url=SpotifyAPIEndpoints.BASE_URL,
            headers={"Authorization": f"Bearer {user.access_token}"},
        ) as client:
            while next:
                if not all and yielded >= limit:
                    client.close()
                    break

                time.sleep(1)

                params = {"limit": limit if limit <= 50 else 50}

                if offset > 0:
                    params["offset"] = offset

                response = client.get(url=next, params=params)

                if response.is_error:
                    self.handle_error(response)

                resp = response.json()

                next = (
                    resp.get("next").replace(f"{SpotifyAPIEndpoints.BASE_URL}/", "")
                    if resp.get("next")
                    else None
                )

                yielded += len(resp.get("items"))

                logger.debug(f"Fetched {yielded} {resp.get("total")}")

                yield from resp.get("items")

    def _library_albums(
        self, user: "AppUser", limit: int = 50, offset: int = 0, all: bool = False
    ) -> typing.Iterable[dict]:
        """Get the user's albums."""
        yielded = 0
        next: str | None = f"{SpotifyAPIEndpoints.SavedAlbums}"

        if all:
            limit = 50  # Default page size is 20

        with httpx.Client(
            base_url=SpotifyAPIEndpoints.BASE_URL,
            headers={"Authorization": f"Bearer {user.access_token}"},
        ) as client:
            while next:
                if not all and yielded >= limit:
                    client.close()
                    break

                time.sleep(1)

                params = {"limit": limit if limit <= 50 else 50}

                if offset > 0:
                    params["offset"] = offset

                response = client.get(url=next, params=params)
                if response.is_error:
                    self.handle_error(response)

                resp = response.json()

                next = resp.get("next")
                if next is not None:
                    next = next.replace(f"{SpotifyAPIEndpoints.BASE_URL}/", "")

                yielded += len(resp.get("items"))

                logger.debug(f"Fetched {yielded} of {resp.get("total")}")

                yield from resp.get("items")

    def _library_artists(
        self,
        user: "AppUser",
        limit: int = 50,
        last: str | None = None,
        all: bool = False,
    ) -> typing.Iterable[dict]:
        """Get the user's followed artists."""
        yielded = 0
        next = f"{SpotifyAPIEndpoints.FollowedArtists}"
        with httpx.Client(
            base_url=SpotifyAPIEndpoints.BASE_URL,
            headers={"Authorization": f"Bearer {user.access_token}"},
        ) as client:
            while next:
                if not all and yielded >= limit:
                    break

                params: dict[str, str | int] = {"limit": limit if limit <= 50 else 50}

                if last is not None:
                    params["after"] = last

                response = client.get(url=next, params={"type": "artist", **params})
                if response.is_error:
                    self.handle_error(response)

                resp = response.json()

                next = resp.get("artists", {}).get("next")

                if next is not None:
                    next = next.replace(f"{SpotifyAPIEndpoints.BASE_URL}/", "")

                if not all:
                    yielded += len(resp.get("artists", {}).get("items"))

                logger.debug(
                    f"Fetched {yielded} {resp.get("artists", {}).get("total")}"
                )

                yield from resp.get("artists", {}).get("items")

    def _library_tracks(
        self, user: "AppUser", limit: int = 50, offset: int = 0, all: bool = False
    ) -> typing.Iterable[dict]:
        """Get the user's saved tracks."""
        yielded = 0
        next = f"{SpotifyAPIEndpoints.SavedTracks}"

        if all:
            limit = 50

        with httpx.Client(
            base_url=SpotifyAPIEndpoints.BASE_URL,
            headers={"Authorization": f"Bearer {user.access_token}"},
        ) as client:
            while next:
                if not all and yielded >= limit:
                    client.close()
                    break

                time.sleep(1)

                params = {"limit": limit if limit <= 50 else 50}

                if offset > 0:
                    params["offset"] = offset

                response = client.get(url=next, params=params)

                if response.is_error:
                    self.handle_error(response)

                resp = response.json()

                next = resp.get("next")

                if next is not None:
                    next = next.replace(f"{SpotifyAPIEndpoints.BASE_URL}/", "")

                yielded += len(resp.get("items"))

                logger.debug(f"Fetched {yielded} {resp.get("total")}")

                yield from resp.get("items")

    def _library_playlist(self, user: "AppUser", playlist_id: str) -> dict:
        """Get the user's playlist.

        1. Get the playlist's metadata.
        2. Get the playlist's tracks (items).
        """
        with httpx.Client(
            base_url=SpotifyAPIEndpoints.BASE_URL,
            headers={"Authorization": f"Bearer {user.access_token}"},
        ) as client:
            response = client.get(
                url=SpotifyAPIEndpoints.Playlist.format(playlist_id=playlist_id)
            )

            if response.is_error:
                self.handle_error(response)

            time.sleep(0.5)

            data = {
                "playlist": response.json(),
                "tracks": list(
                    self._library_playlist_tracks(client, playlist_id),
                ),
            }

            return data

    def _library_playlist_tracks(
        self, client: httpx.Client, playlist_id: str
    ) -> typing.Iterable[dict]:
        """Get the playlist's tracks."""
        next = f"{SpotifyAPIEndpoints.PlaylistTracks.format(playlist_id=playlist_id)}"

        while next:
            response = client.get(url=next, params={"limit": 50})

            if response.is_error:
                self.handle_error(response)

            resp = response.json()

            next = resp.get("next")

            if next is not None:
                time.sleep(0.75)

            yield from resp.get("items")

    def _library_album(self, user: "AppUser", album_id: str) -> dict:
        """Get the user's album."""
        response = httpx.get(
            url=f"{SpotifyAPIEndpoints.BASE_URL}/{SpotifyAPIEndpoints.Album.format(album_id=album_id)}",
            headers={"Authorization": f"Bearer {user.access_token}"},
        )

        if response.is_error:
            self.handle_error(response)

        return response.json()

    def library_album(self, user_pk: int, album_id: str) -> dict:
        """Get the user's album."""
        user = self.get_user(user_pk)

        try:
            return self._library_album(user=user, album_id=album_id)
        except SpotifyExpiredTokenError:
            self.auth_service.refresh_access_token(user.refresh_token)

            user.refresh_from_db()

            return self._library_album(user=user, album_id=album_id)
        except Exception as e:
            logger.error(f"Request to get album {album_id} failed.")
            logger.error(f"Error: {e}")

            raise SpotifyAPIError(str(e)) from e
