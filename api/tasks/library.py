"""Sync operations triggered from library views."""

from celery import shared_task

from api.models import Library, Track
from api.models.music import Album, Artist
from api.models.playlist import Playlist
from api.serializers.library import ExpandedPlaylist


@shared_task
def sync_expanded_playlist(user_pk: int, expanded_playlist: ExpandedPlaylist) -> dict:
    """Sync a playlist and its tracks."""
    result: dict = {
        "library_pk": None,
        "playlist_pk": None,
        "track_pks": [],
        "album_pks": [],
        "artist_pks": [],
        # To replay
        "playlist_spotify_id": expanded_playlist.spotify_id,
    }
    library, _ = Library.objects.get_or_create(user_id=user_pk)
    playlist, _ = Playlist.objects.update_or_create(
        library=library,
        spotify_id=expanded_playlist.spotify_id,
        defaults={
            "name": expanded_playlist.name,
            "public": expanded_playlist.public,
            "shared": expanded_playlist.collaborative,
            "description": expanded_playlist.description,
            "image_url": expanded_playlist.image_url,
            "owner_id": expanded_playlist.owner[0],
            "owner_name": expanded_playlist.owner[1],
        },
    )

    result["library_pk"] = library.pk
    result["playlist_pk"] = playlist.pk

    playlist.libraries.add(library)

    for item in expanded_playlist.tracks:
        album, _ = Album.objects.update_or_create(
            spotify_id=item.album_id,
            defaults={
                "name": item.album_name,
            },
        )

        artists = []
        for artist_id, artist_name in item.artists:
            artist, _ = Artist.objects.update_or_create(
                spotify_id=artist_id,
                defaults={
                    "name": artist_name,
                },
            )

            artists.append(artist)

        track, _ = Track.objects.update_or_create(
            playlist=playlist,
            spotify_id=item.spotify_id,
            album=album,
            defaults={
                "name": item.name,
                "duration_ms": item.duration_ms,
            },
        )

        artist.albums.add(album)
        track.playlists.add(playlist)

        result["track_pks"].append(track.pk)
        result["album_pks"].append(album.pk)
        result["artist_pks"].extend([artist.pk for artist in artists])

    return result
