"""Celery task constants and base classes."""

import uuid

from celery import shared_task

from api.libs.exceptions import SpotifyExpiredTokenError
from api.models.playlist import Playlist
from api.models.users import AppUser
from api.services.spotify import SpotifyLibraryService
from api.services.spotify.auth import SpotifyAuthService

library_service = SpotifyLibraryService()
user_service = SpotifyAuthService()


@shared_task
def sync_user_playlists(user_pk: int) -> list[tuple[uuid.UUID, str]]:
    """Sync playlists from Spotify to the database."""
    user = AppUser.objects.get(pk=user_pk)
    try:
        data = library_service.library_playlists(user=user, all=True)
    except SpotifyExpiredTokenError:
        user_service.refresh_access_token(user.refresh_token)
        user.refresh_from_db()

    data = library_service.library_playlists(user=user, all=True)

    playlists = Playlist.sync.before_sync(data)
    synced = Playlist.sync.sync(playlists=playlists, user_pk=user_pk)

    return list(synced)
