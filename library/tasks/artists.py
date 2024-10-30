"""Artist Syncing Tasks."""

import uuid

from celery import shared_task
from loguru import logger

from api.models import Artist, Library
from api.models.music import Genre
from api.serializers.library import Artist as ArtistSerializer


@shared_task
def sync_artists_from_request(user_id: int, api_artists: list[dict]) -> None:
    """Sync artists from a request."""
    data = [ArtistSerializer(**artist) for artist in api_artists]
    exists = [artist.spotify_id for artist in data]

    library, _ = Library.objects.get_or_create(user_id=user_id)
    qs = library.artists.filter(spotify_id__in=exists, is_synced=True)
    if qs.exists() and qs.count() == len(data):
        logger.info(f"Artists already exist and are synced in library {library.id}")
        return

    for count, item in enumerate(data):
        artist, _ = Artist.objects.get_or_create(
            spotify_id=item.spotify_id,
            defaults={"name": item.name},
        )

        sync_genres_from_artist.s((artist.id), item.genres).apply_async()

        library.artists.add(artist)
        library.save()
        logger.info(f"Synced {count + 1} / {len(data)} artists to library {library.id}")


@shared_task
def sync_genres_from_artist(artist_id: uuid.UUID, genres: list[str]) -> None:
    """Sync genres from an artist."""
    artist = Artist.objects.get(id=artist_id)

    for g in genres:
        genre, _ = Genre.objects.get_or_create(name=g)
        artist.genres.add(genre)

    artist.is_synced = True
    artist.save()

    logger.info(f"Synced {len(genres)} genres to artist {artist.id}")
