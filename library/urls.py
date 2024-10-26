"""URL Config for library."""

from django.urls import path

from library.views import PlaylistViewSet

urlpatterns = [
    path(
        "playlists/<str:playlist_id>",
        PlaylistViewSet.as_view({"get": "retrieve"}),
        name="library-playlist",
    ),
    path(
        "playlists",
        PlaylistViewSet.as_view({"get": "list", "post": "create"}),
        name="library-playlists",
    ),
]
