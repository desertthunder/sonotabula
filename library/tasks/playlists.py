"""Syncing of library data from real-time endpoints."""

from celery import chain, shared_task
from django.db.models import Q
from loguru import logger

from api.models import AppUser, Library, Playlist, Track
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
    library, _ = Library.objects.get_or_create(user_id=user_id)

    exists = Q(spotify_id__in=[playlist.spotify_id for playlist in models])
    snapshot_current = Q(version__in=[playlist.version for playlist in models])
    qs = library.playlists.filter(exists & snapshot_current)

    if qs.count() == len(models):
        logger.info(f"Playlists already added to library {library.id}")
        dispatch_sync_playlist_tracks.s(user_id).apply_async()
        return

    synced = {"count": 0}

    logger.debug(f"User: {user.pk} | {user.spotify_id}, Library: {library.id}")

    for i, playlist in enumerate([playlist.to_db() for playlist in models]):
        logger.info(f"Syncing playlist {playlist.name} to library {library.id}")
        logger.debug(f"Playlist ({i + 1}): {playlist.pk} | {playlist.spotify_id}")
        library.playlists.add(playlist)

        synced["count"] = i

    library.save()

    logger.info(
        f"Synced {synced['count'] + 1} / {len(api_playlists)} playlists to "
        f"library {library.id}"
    )

    dispatch_sync_playlist_tracks.s(user_id).apply_async()


@shared_task
def dispatch_sync_playlist_tracks(user_id: int) -> None:
    """Dispatch a chain of tasks to sync playlist tracks."""
    library = Library.objects.get(user__id=user_id)
    chained = []

    for item, pl in enumerate(library.playlists.filter(is_synced=False).all()):
        if item == 0:
            chained.append(sync_playlist_tracks.s(user_id, pl.spotify_id))
        else:
            chained.append(sync_playlist_tracks.s(pl.spotify_id))

    chain(*chained).apply_async()


@shared_task
def sync_playlist_tracks_from_request(user_id: int, api_playlist: dict) -> None:
    """Sync playlist tracks from a request."""
    logger.warning("TODO (Not implemented)")

    return


@shared_task
def sync_playlist_tracks(user_pk: int, spotify_id: str) -> int:
    """Sync playlist tracks from Spotify to the database."""
    playlist = Playlist.objects.get(spotify_id=spotify_id)
    response = data_service.fetch_playlist_tracks(spotify_id, user_pk)

    cleaned = Track.sync.pre_sync(response)
    data = Track.sync.do(cleaned)
    result = Track.sync.complete_sync(playlist.pk, data)

    logger.debug(f"Synced {str(result)}")

    playlist.is_synced = True
    playlist.save()

    logger.debug(f"Playlist {playlist.pk} is now synced")

    return user_pk
