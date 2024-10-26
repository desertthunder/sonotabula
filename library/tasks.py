"""Syncing of library data from real-time endpoints."""

from celery import shared_task
from django.db.models import Q
from loguru import logger

from api.models.music import Library
from api.models.users import AppUser
from api.serializers.library import Playlist as PlaylistSerializer
from api.services.spotify import (
    SpotifyAuthService,
    SpotifyDataService,
    SpotifyLibraryService,
)

user_service = SpotifyAuthService()
data_service = SpotifyDataService()
library_service = SpotifyLibraryService(user_service)


@shared_task
def sync_playlists_from_request(user_id: int, api_playlists: list[dict]) -> None:
    """Sync playlists from a request."""
    models = [PlaylistSerializer(**playlist) for playlist in api_playlists]
    user = AppUser.objects.get(id=user_id)
    library = Library.objects.get(user_id=user_id)

    exists = Q(spotify_id__in=[playlist.spotify_id for playlist in models])
    snapshot_current = Q(snapshot_id__in=[playlist.version for playlist in models])
    qs = library.playlists.filter(exists & snapshot_current)

    if qs.count() == len(models):
        logger.info(f"Playlists already synced to library {library.id}")
        return

    synced = 0

    logger.debug(f"User: {user.pk} | {user.spotify_id}, Library: {library.id}")

    for i, playlist in enumerate([playlist.to_db() for playlist in models]):
        logger.info(f"Syncing playlist {playlist.name} to library {library.id}")
        logger.debug(f"Playlist ({i + 1}): {playlist.pk} | {playlist.spotify_id}")
        library.playlists.add(playlist)
        synced = i

    library.save()

    logger.info(
        f"Synced {synced + 1} / {len(api_playlists)} playlists to library {library.id}"
    )


@shared_task
def sync_playlist_tracks_from_request(user_id: int, api_playlist: dict) -> None:
    """Sync playlist tracks from a request."""
    pass
