"""API tasks."""

import logging
import typing

from celery import shared_task  # type: ignore

from api.libs.responses import Playlist as PlaylistResponse
from api.models import AppUser, Library, Playlist

logger = logging.getLogger(__name__)


@shared_task
def create_and_add_playlist_to_library(
    playlists: typing.Iterable[PlaylistResponse], user_pk: int
) -> None:
    """Create a playlist with spotify ids."""
    user = AppUser.objects.get(pk=user_pk)
    library, _ = Library.objects.get_or_create(user_id=user)

    for data in playlists:
        playlist, _ = Playlist.objects.get_or_create(
            spotify_id=data.spotify_id, name=data.name, owner_id=data.owner_id
        )

        playlist.image_url = data.image_url
        playlist.version = data.version

        if data.description:
            playlist.description = data.description

        playlist.save()

        library.playlist_ids.add(playlist)

    library.save()
    library.refresh_from_db()

    logger.info(f"Added {len(list(playlists))} playlists to library for user {user_pk}")
