"""Track tasks."""

from celery import shared_task
from django.db.models import Q
from loguru import logger

from api.models import Album, AppUser, Artist, Library, Track
from api.models.analysis import TrackFeatures
from api.serializers.library import Track as TrackSerializer
from api.serializers.library import TrackFeaturesSerializer
from api.serializers.validation.analysis import SyncAnalysis
from api.services.spotify import (
    SpotifyAuthService,
    SpotifyDataService,
    SpotifyLibraryService,
)

AUTH = SpotifyAuthService()
DATA = SpotifyDataService(auth=AUTH)
LIBRARY = SpotifyLibraryService(auth_service=AUTH)


@shared_task
def sync_tracks_from_request(user_id: int, api_tracks: list[dict]) -> None:
    """Sync tracks from a request."""
    models = [TrackSerializer(**t) for t in api_tracks]
    user = AppUser.objects.get(id=user_id)
    library, _ = Library.objects.get_or_create(user_id=user_id)
    spotify_ids = [track.spotify_id for track in models]

    logger.debug(f"User: {user.pk} | {user.spotify_id}, Library: {library.id}")

    exist = Q(spotify_id__in=spotify_ids)
    has_audio_features = Q(features__isnull=False)

    qs = library.tracks.filter(exist & has_audio_features)

    if qs.exists() and qs.count() == len(models):
        logger.info(f"Tracks already added to library {library.id}")

        return

    counts = {"synced": 0, "analyzed": 0}

    audio_features = {
        t["id"]: t for t in DATA.fetch_audio_features(spotify_ids, user_id)
    }

    for i, tr in enumerate(models):
        artist, _ = Artist.objects.get_or_create(
            spotify_id=tr.artist_id, defaults={"name": tr.artist_name}
        )

        album, _ = Album.objects.get_or_create(
            spotify_id=tr.album_id,
            defaults={
                "name": tr.album_name,
                "release_year": int(tr.album_release_date[:4]),
            },
        )
        album.artists.add(artist)
        album.save()

        track, _ = Track.objects.update_or_create(
            spotify_id=tr.spotify_id,
            defaults={
                "album": album,
                "name": tr.name,
                "duration": int(tr.duration_ms),
                "is_synced": True,
                "is_analyzed": False,
            },
        )

        library.tracks.add(track)
        library.save()

        counts["synced"] += i

        if ft := audio_features.get(track.spotify_id):
            cleaned = SyncAnalysis(**ft)
            features = cleaned.model_dump()

            del features["id"]

            track_features, _ = TrackFeatures.objects.update_or_create(
                track=track,
                defaults=features,
            )

            track.is_analyzed = True
            track.save()

            counts["analyzed"] += i

            logger.info(
                f"Recorded features {track_features.id} for track {track.id} |"
                f" {track.spotify_id}"
            )


@shared_task
def sync_track_features_from_request(
    user_id: int, spotify_id: str, api_feature_data: dict
) -> None:
    """Sync audio features from a request."""
    cleaned = TrackFeaturesSerializer(**api_feature_data)
    features = cleaned.model_dump()

    del features["id"]

    library, _ = Library.objects.get_or_create(user_id=user_id)
    track = library.tracks.get(spotify_id=spotify_id)
    track_features, _ = TrackFeatures.objects.update_or_create(
        track=track,
        defaults=features,
    )

    track.is_analyzed = True
    track.save()

    logger.info(
        f"Recorded features {track_features.id} for track {track.id} |"
        f" {track.spotify_id}"
    )
