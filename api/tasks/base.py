"""Celery task constants and base classes."""

import contextlib
import uuid

from celery import shared_task
from django.core.paginator import Paginator
from loguru import logger

from api.models.analysis import Analysis, TrackFeatures
from api.models.music import Album, Library
from api.models.playlist import Playlist
from api.models.track import Track
from api.serializers.library import Track as TrackSerializer
from api.serializers.validation.analysis import SyncAnalysis
from api.services.spotify import (
    SpotifyAuthService,
    SpotifyDataService,
    SpotifyLibraryService,
)
from core.models import AppUser

user_service = SpotifyAuthService()
data_service = SpotifyDataService()
library_service = SpotifyLibraryService(user_service)


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


def sync_saved_tracks(user_pk: int) -> int:
    """Sync saved tracks from Spotify to the database."""
    user = AppUser.objects.get(pk=user_pk)
    library, _ = Library.objects.get_or_create(user=user)
    # (TODO) we should cache this incase we want to retry
    saved_tracks = library_service.library_tracks(user_pk, limit=100)
    cleaned_data = list(TrackSerializer.list(list(saved_tracks)))

    total = len(cleaned_data)
    logger.info(f"Syncing {total} saved tracks for user {user_pk}")

    album: Album | None = None

    for counter, entry in enumerate(cleaned_data):
        with contextlib.suppress(Album.DoesNotExist):
            album = Album.objects.get(spotify_id=entry.album_id)

        if album:
            logger.info(f"Album {album.name} found for track {entry.name}")
            track, _ = Track.objects.get_or_create(
                spotify_id=entry.spotify_id,
                album=album,
                name=entry.name,
                defaults={"duration": entry.duration_ms},
            )
        else:
            logger.info(f"Album not found for track {entry.name}")
            track, _ = Track.objects.get_or_create(
                spotify_id=entry.spotify_id,
                name=entry.name,
                defaults={"duration": entry.duration_ms},
            )

        library.tracks.add(track)

        logger.info(f"Track {track.name} added to library")
        logger.info(f"Synced track {counter + 1} of {total}")

    library.save()

    return library.pk


@shared_task
def sync_saved_tracks_task(user_pk: int) -> int:
    """Sync saved tracks from Spotify to the database."""
    return sync_saved_tracks(user_pk)


def sync_track_features_for_library(user_pk: int) -> int:
    """Sync track features for library tracks."""
    user = AppUser.objects.get(pk=user_pk)
    library, created = Library.objects.get_or_create(user=user)

    if created:
        logger.info("Library created, no tracks to sync")

        return library.pk

    tracks = library.tracks.all().filter(features__isnull=True)

    logger.info(f"User has {tracks.count()} tracks requiring analysis in their library")

    paginated_qs = Paginator(tracks.all(), 100)

    for page in paginated_qs.page_range:
        track_ids = [track.spotify_id for track in paginated_qs.page(page).object_list]
        data = data_service.fetch_audio_features(track_ids, user_pk)

        for entry in data:
            cleaned = SyncAnalysis(**entry)
            track = Track.objects.get(spotify_id=cleaned.id)
            features = cleaned.model_dump()

            del features["id"]

            track_features, _ = TrackFeatures.objects.update_or_create(
                track=track,
                defaults=features,
            )

            logger.info(f"Track features ({track_features.pk}) added for {track.name}")

    return library.pk


@shared_task
def sync_track_features_for_library_task(user_pk: int) -> int:
    """Sync track features for library tracks."""
    return sync_track_features_for_library(user_pk)


@shared_task
def sync_saved_artists_task(user_pk: int) -> list[tuple[uuid.UUID, str]]:
    """Sync saved artists from Spotify to the database."""
    # Fetch saved artists from Spotify

    # Clean the data

    # Add the data to the user's library

    # Return the result
    raise NotImplementedError


@shared_task
def sync_genres_task(user_pk: int) -> list[uuid.UUID]:
    """Sync genres to the database."""
    # Get all user's artists from the database
    # (query library)

    # Fetch genres for each artist

    # Clean the data

    # Add the data to the database

    # Return the result
    raise NotImplementedError
