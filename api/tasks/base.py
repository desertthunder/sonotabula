"""Celery task constants and base classes."""

import uuid

from celery import shared_task

from api.libs.exceptions import SpotifyExpiredTokenError
from api.models.analysis import Analysis
from api.models.music import Library
from api.models.playlist import Playlist
from api.models.track import Track
from api.models.users import AppUser
from api.services.spotify import SpotifyLibraryService
from api.services.spotify.auth import SpotifyAuthService
from api.services.spotify.data import SpotifyDataService

library_service = SpotifyLibraryService()
user_service = SpotifyAuthService()
data_service = SpotifyDataService()


@shared_task
def sync_user_playlists(user_pk: int) -> list[tuple[uuid.UUID, str]]:
    """Sync playlists from Spotify to the database."""
    user = AppUser.objects.get(pk=user_pk)
    library, _ = Library.objects.get_or_create(user_id=user_pk)

    try:
        data = library_service.library_playlists(user=user, all=True)
    except SpotifyExpiredTokenError:
        user_service.refresh_access_token(user.refresh_token)
        user.refresh_from_db()

    data = library_service.library_playlists(user=user, all=True)

    playlists = Playlist.sync.before_sync(data)
    synced = Playlist.sync.sync(playlists=playlists, user_pk=user_pk)

    result = list(synced)
    library.playlists.add(*[playlist_id for playlist_id, _ in result])  # type: ignore

    return list(synced)


@shared_task
def sync_playlist_tracks(spotify_id: str, user_pk: int) -> str:
    """Sync playlist tracks from Spotify to the database."""
    user = AppUser.objects.get(pk=user_pk)
    playlist = Playlist.objects.get(spotify_id=spotify_id)

    try:
        response = data_service.fetch_playlist_tracks(playlist_id=spotify_id, user=user)
    except SpotifyExpiredTokenError:
        user_service.refresh_access_token(user.refresh_token)
        user.refresh_from_db()

        response = data_service.fetch_playlist_tracks(playlist_id=spotify_id, user=user)

    data = Track.sync.before_sync(response)
    result = Track.sync.sync(data)

    playlist.tracks.clear()
    playlist.tracks.add(*[track_id for track_id, _ in result])  # type: ignore
    playlist.is_synced = True
    playlist.save()

    return playlist.spotify_id


@shared_task
def sync_track_analysis_for_playlist(playlist_pk: uuid.UUID, user_pk: int) -> uuid.UUID:
    """Sync track analysis for a playlist."""
    user = AppUser.objects.get(pk=user_pk)

    track_ids = Analysis.sync.pre_analysis(playlist_pk, user_pk)
    try:
        data = data_service.fetch_audio_features(track_ids, user)
    except SpotifyExpiredTokenError:
        user_service.refresh_access_token(user.refresh_token)
        user.refresh_from_db()

        data = data_service.fetch_audio_features(track_ids, user)

    return Analysis.sync.analyze(str(playlist_pk), user_pk, data)
