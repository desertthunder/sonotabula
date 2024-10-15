"""Script to perform analysis of a spotify wrapped."""

import time

from loguru import logger

from api.models import Album, Analysis, AppUser, Artist, Genre, Library, Playlist
from api.models.analysis import Computation, ComputationValidator
from api.serializers.library import Album as AlbumSerializer
from api.services.spotify import (
    SpotifyAuthService,
    SpotifyDataService,
    SpotifyLibraryService,
)

data_service = SpotifyDataService()
auth_service = SpotifyAuthService()
library_service = SpotifyLibraryService(auth_service=auth_service)


def main() -> None:
    """Main function."""
    user = AppUser.objects.get(is_staff=True)

    logger.info(f"User: {user.spotify_id} | {user.pk}")

    library = Library.objects.get(user=user)

    logger.info(f"Library: {library.pk}")

    playlists = Playlist.objects.filter(
        libraries__in=[library], is_synced=True, name__icontains="your top songs"
    ).all()

    logger.info(f"Got {len(playlists)} playlists.")

    for playlist in playlists:
        logger.info(f"Processing playlist: {playlist.pk} | {playlist.name}")

        track_ids = Analysis.sync.pre_analysis(playlist.pk, user.pk)
        feature_data = data_service.fetch_audio_features(track_ids, user.pk)
        time.sleep(3)
        result = Analysis.sync.analyze(
            playlist_pk=str(playlist.pk),
            user_pk=user.pk,
            items=feature_data,
        )

        logger.info(f"Created/Found analysis: {result}")

        analysis = Analysis.objects.get(pk=result)

        logger.info(f"Analysis: {analysis.pk} | {analysis.playlist_id}")

        analysis_pk = analysis.pk
        data = Analysis.sync.compute(analysis_pk)

        logger.info(f"Computed analysis: {data.keys()}")

        computation, created = Computation.objects.update_or_create(
            analysis=analysis,
            playlist=playlist,
            defaults={"data": ComputationValidator(**data).model_dump()},
        )

        if created:
            logger.info(f"Created computation: {computation.pk}")
        else:
            logger.info(f"Updated computation: {computation.pk}")

        logger.info(f"Saved computation for {analysis_pk} | {playlist.pk}")

        time.sleep(1)

    logger.info("Done.")


def sync_my_albums() -> None:
    """Sync albums."""
    user = AppUser.objects.get(is_staff=True)

    logger.info(f"User: {user.spotify_id} | {user.pk}")

    library = Library.objects.get(user=user)

    albums = library_service.library_albums(user.pk, all=True)
    albums_ = list(albums)

    cleaned_albums = AlbumSerializer.list(albums_)
    total = len(albums_)

    for counter, cleaned in enumerate(cleaned_albums):
        logger.info(f"Processing album: {cleaned.spotify_id} | {cleaned.name}")

        # album_type, name, spotify_id, label, copyright, release_year
        artist, _ = Artist.objects.get_or_create(
            name=cleaned.artist_name,
            spotify_id=cleaned.artist_id,
        )

        album, _ = Album.objects.update_or_create(
            spotify_id=cleaned.spotify_id,
            name=cleaned.name,
            defaults={
                "is_synced": True,
                "release_year": cleaned.release_date.split("-")[0],
                "image_url": cleaned.image_url,
                "label": cleaned.label,
            },
        )

        if album_genres := cleaned.genres:
            for genre_name in album_genres:
                genre, _ = Genre.objects.get_or_create(name=genre_name)

                album.genres.add(genre)
                artist.genres.add(genre)

                artist.save()
                logger.info(f"Added genre: {genre.pk} | {genre.name}")

        album.artists.add(artist)
        album.libraries.add(library)
        album.save()

        logger.info(f"Artist: {artist.pk} | {artist.name}")
        logger.info(f"Saved album {counter} of {total}: {album.pk} | {album.name}")

        time.sleep(1)

    logger.info("Done. 🚀")


if __name__ == "__main__":
    main()
