"""Script to perform analysis of a spotify wrapped."""

import time

from loguru import logger

from api.models import Analysis, AppUser, Library, Playlist
from api.models.analysis import Computation, ComputationValidator
from api.services.spotify import SpotifyDataService

data_service = SpotifyDataService()


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


if __name__ == "__main__":
    main()
