from library.tasks.artists import sync_artists_from_request, sync_genres_from_artist
from library.tasks.playlists import sync_and_add_playlists_to_library
from library.tasks.track import (
    sync_track_features_from_request,
    sync_tracks_from_request,
)
