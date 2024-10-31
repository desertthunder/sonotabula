"""Playlist Browser Tasks.

Tasks for syncing and analyzing playlists and their tracks.

Any task with user_id as an argument makes an API call.
"""

import time
import typing
import uuid

from celery import group, shared_task
from loguru import logger

from api.models import Playlist
from api.models.analysis import Analysis, Computation
from api.models.track import Track
from api.services.spotify import (
    SpotifyAuthService,
    SpotifyDataService,
    SpotifyLibraryService,
)
from browser.models import Library

AUTH = SpotifyAuthService()
LIBRARY = SpotifyLibraryService(auth_service=AUTH)
DATA = SpotifyDataService()


class PlaylistTask:
    """Playlist task base class."""

    user_id: int
    playlist_id: uuid.UUID
    status: str = "PENDING"

    def __init__(self, user_id: int, playlist_id: uuid.UUID) -> None:
        """Create a new task for a playlist."""
        self.user_id = user_id
        self.playlist_id = playlist_id

    def _run(self, *args, **kwargs) -> None:
        raise NotImplementedError("Subclasses must implement _run.")

    def __call__(self) -> typing.Self:
        """Run the playlist analysis chain."""
        try:
            self.status = "RUNNING"
            self._run()
            self.status = "SUCCESS"
        except Exception as e:
            logger.error(e)
            self.status = "FAILURE"

        return self


class PlaylistSync(PlaylistTask):
    """Collection of tasks for syncing playlists."""

    def sync(self) -> tuple[list[dict], uuid.UUID]:
        """Dispatch playlist sync."""
        library, _ = Library.objects.get_or_create(user_id=self.user_id)
        playlist = Playlist.objects.get(id=self.playlist_id)
        response = LIBRARY.library_playlist(self.user_id, playlist.spotify_id)

        if data := response.get("playlist"):
            cleaned = Playlist.sync.clean_playlist(data)
            playlist = Playlist.sync.sync_playlist(cleaned.model_dump(), self.user_id)
            library.playlists.add(playlist)

            pk = Playlist.sync.complete_playlist_sync(playlist)

            return response.get("tracks", []), pk

        raise ValueError(f"Failed to sync playlist {self.playlist_id}.")

    def track_sync(self, data: tuple[list[dict], uuid.UUID]) -> uuid.UUID:
        """Dispatch track analysis."""
        response, playlist_id = data
        cleaned = Track.sync.pre_sync(response)
        synced = Track.sync.do(cleaned)
        complete = Track.sync.complete_sync(playlist_id, synced)
        return complete

    def complete(self, playlist_id: uuid.UUID) -> uuid.UUID:
        """Mark the playlist as analyzed."""
        playlist = Playlist.objects.get(id=playlist_id)
        playlist.is_synced = True
        playlist.save()

        logger.info(f"Marked {playlist_id} as synced.")

        return playlist_id

    def _run(self) -> None:
        """Run the playlist sync chain."""
        sync_result = self.sync()
        track_result = self.track_sync(sync_result)

        self.complete(track_result)


class PlaylistAnalysis(PlaylistTask):
    """Collection of tasks for analyzing playlists."""

    def analysis(self) -> uuid.UUID:
        """Dispatch playlist analysis."""
        logger.info(f"Analyzing playlist {self.playlist_id}.")
        track_ids = Analysis.sync.pre_analysis(self.playlist_id, self.user_id)
        data = DATA.fetch_audio_features(track_ids, self.user_id)

        time.sleep(1)

        analyzed = Analysis.sync.analyze(self.playlist_id, self.user_id, data)

        return analyzed

    def computation(self, analysis_id: uuid.UUID) -> uuid.UUID:
        """Dispatch analysis computation."""
        logger.info(f"Computing analysis {analysis_id}.")
        computations = Analysis.sync.compute(analysis_id)
        computed = Analysis.sync.set_computation(analysis_id, computations)

        return computed

    def complete(self, computation_id: uuid.UUID) -> None:
        """Mark the playlist as analyzed."""
        computation = Computation.objects.prefetch_related(
            "playlist",
        ).get(id=computation_id)
        playlist = computation.playlist
        playlist.is_analyzed = True
        playlist.save()

        logger.info(f"Marked {playlist.id} as analyzed.")

        return None

    def _run(self) -> None:
        """Run the playlist analysis chain."""
        analysis_result = self.analysis()
        computation_result = self.computation(analysis_result)
        logger.debug(f"Analysis result: {analysis_result}")
        logger.debug(f"Computation result: {computation_result}")

        self.complete(computation_result)


@shared_task
def analyze_playlist(playlist_id: uuid.UUID, user_id: int) -> str:
    """Analyze a playlist.

    Creates a chain for a playlist:
        1. Fetch and analyze the playlist tracks.
        2. Perform computations on the analysis data.
        3. Mark the playlist as analyzed.
    """
    runner = PlaylistAnalysis(user_id, playlist_id)

    runner.__call__()

    return runner.status


@shared_task
def sync_playlist(playlist_id: uuid.UUID, user_id: int) -> str:
    """Sync library playlists.

    Creates a chain for each playlist (using the primary key):
        1. Sync the playlist
        2. Sync its tracks and associate them with the playlist
        3. Mark the playlist as synced
    Once the first chain is complete, the playlist is analyzed.

    Puts the chains in a group and applies them asynchronously.
    """
    runner = PlaylistSync(user_id, playlist_id)

    runner.__call__()

    return runner.status


@shared_task
def sync_playlists(user_id: int, playlist_ids: list[uuid.UUID]) -> None:
    """Sync multiple playlists."""
    tasks = [
        group(
            sync_playlist.s(playlist_id, user_id),
            analyze_playlist.s(playlist_id, user_id),
        )
        for playlist_id in playlist_ids
    ]

    group(tasks).apply_async()
