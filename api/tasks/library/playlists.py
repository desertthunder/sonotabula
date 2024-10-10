"""Asynchronous playlist tasks.

Parking Lot
- TODO: Batch requests
    - Audio Features: 100 tracks per request
    - Artists: 50 artists per request
    - Tracks: 50 tracks per request
- TODO: tests
"""

import datetime
import time

from celery import shared_task

from api.models.analysis import Analysis, TrackFeatures
from api.models.music import Album, Artist, Genre, Playlist, Track
from api.models.serializers import (
    Artist as ArtistSerializer,
)
from api.models.serializers import (
    PlaylistAlbum,
    PlaylistTrack,
    SimplePlaylist,
)
from api.models.serializers import (
    TrackFeatures as TrackFeaturesSerializer,
)
from api.models.users import AppUser
from api.services.spotify import SpotifyAnalysisService

analysis_service = SpotifyAnalysisService()


@shared_task
def fetch_artist(artist_id: str, user_pk: int) -> None:
    """Fetch artist from Spotify API and store in database."""
    user = AppUser.objects.get(pk=user_pk)
    response = analysis_service.get_artist(artist_id, user)
    time.sleep(1)
    data = ArtistSerializer.build(response)

    artist, _ = Artist.objects.update_or_create(
        spotify_id=data.spotify_id,
        defaults={
            "name": data.name,
            "image_url": data.image_url,
            "spotify_follower_count": data.spotify_follower_count,
        },
    )

    for g in data.genres:
        genre, _ = Genre.objects.get_or_create(name=g)
        artist.genre_ids.add(genre)
        genre.artist_ids.add(artist)
        genre.save()

    artist.save()


@shared_task
def fetch_track_features(playlist_pk: int, user_pk: int, track_pk: int) -> None:
    """Fetch track features from Spotify API and store in database.

    Then build an analysis record.
    """
    playlist = Playlist.objects.get(pk=playlist_pk)
    user = AppUser.objects.get(pk=user_pk)
    track = Track.objects.get(pk=track_pk)

    response = analysis_service.get_track_features(track.spotify_id, user)
    time.sleep(1)
    data = TrackFeaturesSerializer(**response)

    # TODO: Limits need to be imposed here

    _ = TrackFeatures.objects.update_or_create(
        track_id=track.pk,
        defaults={**data.model_dump()},
    )

    # Build analysis record
    analysis, _ = Analysis.objects.get_or_create(
        playlist_id=playlist,
        user_id=user,
        version=playlist.version,
    )

    analysis.tracks.add(track)
    analysis.save()


@shared_task
def fetch_playlist_tracks(playlist_id: str, user_pk: int) -> None:
    """Fetch tracks for a playlist from Spotify API and store in database."""
    user = AppUser.objects.get(pk=user_pk)
    playlist = Playlist.objects.get(spotify_id=playlist_id, user_id=user)

    try:
        analysis = Analysis.objects.get(playlist_id=playlist.pk)

        # If analysis exists AND was created within the last 24 hours,
        # skip this task.
        time_delta = datetime.datetime.now() - datetime.timedelta(days=1)
        if analysis.created_at > time_delta:
            return
    except Analysis.DoesNotExist:
        pass

    for item in analysis_service.get_playlist_tracks(playlist_id, user):
        # Create track
        time.sleep(0.5)
        data = PlaylistTrack.build(item)
        track, _ = Track.objects.update_or_create(
            spotify_id=data.spotify_id,
            defaults={
                "name": data.name,
                "duration": data.duration,
            },
        )

        album_data = item.get("track", {}).get("album", {})
        serialized_album = PlaylistAlbum.build(album_data)
        album, _ = Album.objects.update_or_create(
            spotify_id=serialized_album.spotify_id,
            defaults={
                "name": serialized_album.name,
                "image_url": serialized_album.image_url,
                "album_type": serialized_album.album_type,
                "release_year": serialized_album.release_year.split("-")[0],
            },
        )

        track.album_id = album
        track.save()

        fetch_track_features.delay(playlist.pk, user.pk, track.pk)

        # Add track to playlist
        playlist.track_ids.add(track)
        playlist.save()

        for artist_id in data.artist_ids:
            fetch_artist.delay(artist_id, user.pk)


@shared_task
def fetch_playlists(user_pk: int) -> None:
    """Fetch playlists from Spotify API and store in database."""
    user = AppUser.objects.get(pk=user_pk)
    for item in analysis_service.get_all_playlists(user):
        # Create playlist
        time.sleep(0.5)
        data = SimplePlaylist.build(item)

        playlist, _ = Playlist.objects.update_or_create(
            spotify_id=data.spotify_id,
            defaults={
                "version": data.version,
                "image_url": data.image_url,
                "public": data.public,
                "shared": data.shared,
                "description": data.description,
                "user_id": user,
                "owner_id": data.owner_id,
            },
        )

        # Fetch tracks
        fetch_playlist_tracks.delay(playlist.spotify_id, user.pk)
