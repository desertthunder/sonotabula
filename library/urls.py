"""URL Config for library."""

from django.urls import path

from library.views import PlaylistViewSet, TrackViewSet

urlpatterns = [
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
    path("tracks", TrackViewSet.as_view({"get": "list"}), name="library-tracks"),
]
