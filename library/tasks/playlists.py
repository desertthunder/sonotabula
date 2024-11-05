"""Syncing of library data from real-time endpoints."""

import time
import typing

from celery import Task, shared_task, states
from celery.signals import task_postrun, task_prerun
from django.db.models import Q
from loguru import logger

from api.models import Playlist, Track
from api.services.spotify import (
    SpotifyAuthService,
    SpotifyDataService,
    SpotifyLibraryService,
)
from browser.models import Library
from core.models import AppUser
from library.serializers import PlaylistAPISerializer
from live.models import Notification
from live.signals import notify_failure, notify_success

user_service = SpotifyAuthService()
data_service = SpotifyDataService()
library_service = SpotifyLibraryService(user_service)


@shared_task
def sync_and_add_playlists_to_library(
    user_id: int, api_playlists: list[dict]
) -> tuple[int, str, list[tuple[str, str]]]:
    """Sync playlists from a request."""
    logger.info(f"Syncing playlists for user {user_id}")

    models = [PlaylistAPISerializer(**playlist) for playlist in api_playlists]
    user = AppUser.objects.get(id=user_id)
    library, _ = Library.objects.get_or_create(user_id=user_id)

    exists = Q(spotify_id__in=[playlist.spotify_id for playlist in models])
    snapshot_current = Q(version__in=[playlist.version for playlist in models])
    qs = library.playlists.filter(exists & snapshot_current)

    if qs.count() == len(models):
        logger.info(f"Playlists already added to library {library.id}")
        return (
            user_id,
            str(library.id),
            [(str(playlist.id), playlist.spotify_id) for playlist in qs.all()],
        )

    synced = {"count": 0}

    logger.debug(f"User: {user.pk} | {user.spotify_id}, Library: {library.id}")

    playlists: list[Playlist] = [playlist.to_db() for playlist in models]
    for i, playlist in enumerate(playlists):
        logger.info(f"Syncing playlist {playlist.name} to library {library.id}")
        logger.debug(f"Playlist ({i + 1}): {playlist.pk} | {playlist.spotify_id}")
        library.playlists.add(playlist)

        synced["count"] = i

    library.save()

    logger.info(
        f"Synced {synced['count'] + 1} / {len(api_playlists)} playlists to "
        f"library {library.id}"
    )

    for playlist in playlists:
        spotify_id = playlist.spotify_id

        logger.info(
            f"Syncing playlist tracks for {playlist.pk} | {playlist.spotify_id}"
        )

        time.sleep(0.5)
        response = data_service.fetch_playlist_tracks(spotify_id, user_id)
        time.sleep(0.5)

        cleaned = Track.sync.pre_sync(response)
        data = Track.sync.do(cleaned)
        result = Track.sync.complete_sync(playlist.pk, data)

        logger.debug(f"Synced {str(result)}")

        playlist.is_synced = True
        playlist.save()

        logger.debug(f"Playlist {playlist.pk} is now synced")

    return (
        user_id,
        str(library.id),
        [
            (
                str(playlist.id),
                playlist.spotify_id,
            )
            for playlist in playlists
        ],
    )


@task_prerun.connect(sender=sync_and_add_playlists_to_library)
def sync_playlists_start(
    sender: typing.Callable, task_id: str, task: Task, **kwargs
) -> None:
    """Log when the task starts."""
    args = task.request.args

    if not args:
        logger.error("No arguments provided to task")

        return

    user_id = args[0]
    library, _ = Library.objects.get_or_create(user_id=user_id)
    notification = Notification.objects.create(
        user_id=user_id,
        task_id=task_id,
        resource_id=library.id,
        operation=Notification.Operations.SYNC,
        resource=Notification.Resources.LIBRARY,
        extras={},
    )

    logger.info(f"Task {task_id} started")
    logger.info(f"Notification {notification.id} created")


@task_postrun.connect(sender=sync_and_add_playlists_to_library)
def sync_playlists_complete(sender: typing.Callable, *args, **kwargs) -> None:
    """Log when the task is successful."""
    if task_id := kwargs.get("task_id"):
        logger.info(f"Task {task_id} completed.")

        notification = Notification.objects.get(task_id=task_id)

        state = kwargs.get("state", "UNKNOWN")

        if state == states.SUCCESS:
            notify_success.send(sender=Notification, instance=notification)
            logger.info("Task completed successfully.")

        if state == states.FAILURE:
            notify_failure.send(sender=Notification, instance=notification)
            logger.error("Task failed.")
