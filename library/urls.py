"""URL Config for library."""

from django.urls import path

from library.views import AlbumViewSet, ArtistViewSet, PlaylistViewSet, TrackViewSet

urlpatterns = [
    path("artists", ArtistViewSet.as_view({"get": "list"}), name="library-artists"),
    path("albums", AlbumViewSet.as_view({"get": "list"}), name="library-albums"),
    path(
        "playlists/<str:spotify_id>",
        PlaylistViewSet.as_view({"get": "retrieve"}),
        name="library-playlist",
    ),
    path(
        "playlists",
        PlaylistViewSet.as_view({"get": "list", "post": "create"}),
        name="library-playlists",
    ),
    path(
        "tracks/<str:spotify_id>/analysis",
        TrackViewSet.as_view({"get": "data"}),
        name="library-track-analysis",
    ),
    path(
        "tracks/<str:spotify_id>",
        TrackViewSet.as_view({"get": "retrieve"}),
        name="library-track",
    ),
    path(
        "tracks",
        TrackViewSet.as_view({"get": "list", "post": "create"}),
        name="library-tracks",
    ),
]
