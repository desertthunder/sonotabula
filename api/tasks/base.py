"""Celery task constants and base classes."""

import uuid

from celery import shared_task

from api.models.analysis import Analysis
from api.models.music import Library
from api.models.playlist import Playlist
from api.models.track import Track
from api.services.spotify import (
    SpotifyAuthService,
    SpotifyDataService,
    SpotifyLibraryService,
)

library_service = SpotifyLibraryService()
user_service = SpotifyAuthService()
data_service = SpotifyDataService()


@shared_task
def sync_user_playlists(user_pk: int) -> list[tuple[uuid.UUID, str]]:
    """Sync playlists from Spotify to the database."""
    library, _ = Library.objects.get_or_create(user_id=user_pk)

    data = library_service.library_playlists(user_pk, all=True)

    cleaned = Playlist.sync.pre_sync(data)
    synced = Playlist.sync.do(playlists=cleaned, user_pk=user_pk)
    result = Playlist.sync.complete_sync(library.pk, synced)

    return result


@shared_task
def sync_playlist_tracks(spotify_id: str, user_pk: int) -> tuple[uuid.UUID, str]:
    """Sync playlist tracks from Spotify to the database."""
    playlist = Playlist.objects.get(spotify_id=spotify_id)
    response = data_service.fetch_playlist_tracks(spotify_id, user_pk)

    cleaned = Track.sync.pre_sync(response)
    data = Track.sync.do(cleaned)
    result = Track.sync.complete_sync(playlist.pk, data)
    return (result, playlist.spotify_id)


@shared_task
def sync_track_analysis_for_playlist(playlist_pk: uuid.UUID, user_pk: int) -> uuid.UUID:
    """Sync track analysis for a playlist."""
    track_ids = Analysis.sync.pre_analysis(playlist_pk, user_pk)
    data = data_service.fetch_audio_features(track_ids, user_pk)
    return Analysis.sync.analyze(str(playlist_pk), user_pk, data)
