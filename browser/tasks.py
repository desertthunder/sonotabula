"""Playlist Browser Tasks.

Tasks for syncing and analyzing playlists and their tracks.

Any task with user_id as an argument makes an API call.
"""

import enum
import time
import typing
import uuid

from celery import group, shared_task
from celery.states import FAILURE, PENDING, SUCCESS
from loguru import logger

from api.blocks import AlbumArtistSyncBlock, AlbumSyncBlock, AlbumTrackSyncBlock
from api.models import Playlist
from api.models.album import Album
from api.models.analysis import Analysis, Computation
from api.models.music import Artist
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


class TaskStatus(enum.StrEnum):
    """Task status."""

    Running = PENDING
    Success = SUCCESS
    Failed = FAILURE


@shared_task
def pause_execution_task(seconds: int = 5) -> None:
    """Pause execution for a given number of seconds."""
    time.sleep(seconds)

    return None


class Task:
    """Task base class."""

    status: TaskStatus

    def _run(self, *args, **kwargs) -> None:
        raise NotImplementedError("Subclasses must implement _run.")

    def __call__(self, *args, **kwargs) -> typing.Self:
        """Run the album analysis chain."""
        try:
            self.status = TaskStatus.Running
            self._run(*args, **kwargs)
            self.status = TaskStatus.Success
        except Exception as e:
            self.status = TaskStatus.Failed
            logger.error(e)

            raise e from e

        return self


############################################
# Playlist Tasks                           #
############################################


class PlaylistTask(Task):
    """Playlist task base class."""

    user_id: int
    playlist_id: uuid.UUID

    def __init__(self, user_id: int, playlist_id: uuid.UUID) -> None:
        """Create a new task for a playlist."""
        self.user_id = user_id
        self.playlist_id = playlist_id


class PlaylistSync(PlaylistTask):
    """Collection of tasks for syncing playlists."""

    def pre_flight(self) -> bool:
        """Check the version of the playlist and skip if it's already synced.

        Tells us if we *should* sync the playlist.
        """
        playlist = Playlist.objects.get(id=self.playlist_id)

        if playlist.is_synced:
            response = LIBRARY.library_playlist(self.user_id, playlist.spotify_id)

            if (
                snapshot_id := response.get("snapshot_id")
            ) and snapshot_id == playlist.version:
                logger.info(
                    f"Playlist {self.playlist_id} has already been synced. Skipping."
                )

                return False

        return True

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
        if not self.pre_flight():
            return

        time.sleep(1)  # Pause after the preflight API call
        sync_result = self.sync()
        track_result = self.track_sync(sync_result)

        self.complete(track_result)


class PlaylistAnalysis(PlaylistTask):
    """Collection of tasks for analyzing playlists."""

    def pre_flight(self) -> bool:
        """Check that the playlist has been synced and analyzed.

        Skip the analysis if the playlist has already been analyzed.
        """
        playlist = Playlist.objects.get(id=self.playlist_id)
        if playlist.is_analyzed:
            logger.info(
                f"Playlist {self.playlist_id} has already been analyzed. Skipping."
            )
            return False

        return True

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

        if playlist := computation.playlist:
            playlist.is_analyzed = True
            playlist.save()
            logger.info(f"Marked {playlist.id} as analyzed.")

            return

        logger.error(f"Failed to mark {computation_id} as analyzed.")

    def _run(self) -> None:
        """Run the playlist analysis chain."""
        if not self.pre_flight():
            return

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
def sync_and_analyze_playlist(playlist_id: uuid.UUID, user_id: int) -> None:
    """Sync and analyze a playlist."""
    group(
        sync_playlist.s(
            playlist_id,
            user_id,
        ),
        pause_execution_task.s(5),
        analyze_playlist.s(
            playlist_id,
            user_id,
        ),
    ).apply_async()


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


############################################
# Album Tasks                              #
############################################


class AlbumTask(Task):
    """Album task base class."""

    user_id: int
    album_id: uuid.UUID | None = None

    def __init__(self, user_id: int, album_id: uuid.UUID | None = None) -> None:
        """Create a new task for an album."""
        self.user_id = user_id
        self.album_id = album_id


class AlbumSync(AlbumTask):
    """Sync album."""

    cleaned_album: AlbumSyncBlock
    cleaned_artists: list[AlbumArtistSyncBlock]
    cleaned_tracks: list[AlbumTrackSyncBlock]

    def sync_albums(self) -> list[uuid.UUID]:
        """Sync albums."""
        library = Library.objects.get(user_id=self.user_id)
        response = LIBRARY.library_albums(self.user_id, limit=10)
        albums = []
        for item in response:
            cleaned = Album.sync.clean_data(item.get("album", {}))
            album = Album.sync.sync_data(cleaned)
            albums.append(album)

            logger.info("Synced album {album.pk}.")
            library.albums.add(album)
            library.save()

            for art in cleaned.artists:
                artist = Artist.sync.sync_album_artist(album, art)
                logger.info(f"Synced artist {artist.pk} for album {album.pk}.")

            for tr in cleaned.tracks:
                track = Track.sync.sync_album_track(album, tr)
                logger.info(f"Synced track {track.pk} for album {album.pk}.")

        return [album.id for album in albums]

    def sync_album(self) -> uuid.UUID:
        """Sync album."""
        library = Library.objects.get(user_id=self.user_id)
        if not self.album_id:
            raise ValueError("Album ID is required.")

        album = Album.objects.get(id=self.album_id)

        response = LIBRARY.library_album(self.user_id, album.spotify_id)
        time.sleep(1)

        if data := response.get("album"):
            self.cleaned_album = Album.sync.clean_data(data)

            album = Album.sync.sync_data(self.cleaned_album)
            library.albums.add(album)
            library.save()

            self.cleaned_artists = self.cleaned_album.artists
            self.cleaned_tracks = self.cleaned_album.tracks

            return album.id

        raise ValueError(f"Failed to sync album {self.album_id}.")

    def sync_album_artists(self) -> uuid.UUID:
        """Sync album artists."""
        if not self.album_id:
            raise ValueError("Album ID is required.")

        album = Album.objects.get(id=self.album_id)

        for artist in self.cleaned_artists:
            Artist.sync.sync_album_artist(album, artist)

        return self.album_id

    def sync_album_tracks(self, album_id: uuid.UUID) -> uuid.UUID:
        """Sync album tracks."""
        album = Album.objects.get(id=album_id)

        for tr in self.cleaned_tracks:
            track = Track.sync.sync_album_track(album, tr)

            logger.info(f"Synced track {track.pk} for album {album.pk}.")

        return album_id

    def complete(self, album_id: uuid.UUID) -> None:
        """Mark the album as synced."""
        album = Album.objects.get(id=album_id)
        album.is_synced = True
        album.save()

        logger.info(f"Marked {album_id} as synced.")

        return None

    def _run(self, many: bool = False) -> None:
        """Run the album sync chain."""
        try:
            if many:
                logger.debug("Syncing multiple albums.")
                album_ids = self.sync_albums()

                for album_id in album_ids:
                    self.complete(album_id)
            else:
                album_id = self.sync_album()
                album_id = self.sync_album_artists()
                track_id = self.sync_album_tracks(album_id)

                self.complete(track_id)
        except Exception as e:
            self.status = TaskStatus.Failed
            logger.error(e)
            raise e from e


class AlbumAnalysis(AlbumTask):
    """Analyze album."""

    def analysis(self) -> uuid.UUID:
        """Dispatch album analysis."""
        if not self.album_id:
            raise ValueError("Album ID is required.")

        logger.info(f"Analyzing album {self.album_id}.")
        track_ids = Analysis.sync.prep_album(self.album_id, self.user_id)
        data = DATA.fetch_audio_features(track_ids, self.user_id)

        time.sleep(1)

        analyzed = Analysis.sync.analyze_album(self.album_id, self.user_id, data)

        return analyzed

    def computation(self, analysis_id: uuid.UUID) -> uuid.UUID:
        """Dispatch analysis computation."""
        logger.info(f"Computing analysis {analysis_id}.")
        computations = Analysis.sync.compute(analysis_id)
        computed = Analysis.sync.set_computation(analysis_id, computations)

        return computed

    def complete(self, computation_id: uuid.UUID) -> None:
        """Mark the album as analyzed."""
        computation = Computation.objects.prefetch_related(
            "album",
        ).get(id=computation_id)

        if album := computation.album:
            album.is_analyzed = True
            album.save()

            logger.info(f"Marked {album.id} as analyzed.")

            return

        logger.error(f"Failed to mark {computation_id} as analyzed.")

    def _run(self) -> None:
        """Run the album analysis chain."""
        analysis_result = self.analysis()
        computation_result = self.computation(analysis_result)
        logger.debug(f"Analysis result: {analysis_result}")
        logger.debug(f"Computation result: {computation_result}")

        self.complete(computation_result)


@shared_task
def sync_albums(user_id: int) -> str:
    """Sync albums.

    Creates a chain for each album:
        1. Sync the album
        2. Sync its artists
        3. Sync its tracks
        4. Mark the album as synced
    """
    runner = AlbumSync(user_id)

    runner.__call__(many=True)

    return runner.status


@shared_task
def sync_album(album_id: uuid.UUID, user_id: int) -> str:
    """Sync album.

    Creates a chain for an album:
        1. Sync the album
        2. Sync its artists
        3. Sync its tracks
        4. Mark the album as synced
    """
    runner = AlbumSync(user_id, album_id)

    runner.__call__()

    return runner.status


@shared_task
def analyze_album(album_id: uuid.UUID, user_id: int) -> str:
    """Analyze an album.

    Creates a chain for an album:
        1. Fetch and analyze the album tracks.
        2. Perform computations on the analysis data.
        3. Mark the album as analyzed.
    """
    runner = AlbumAnalysis(user_id, album_id)

    runner.__call__()

    return runner.status
