"""Browser URL configuration."""

from django.urls import path

from browser.views import PlaylistMetaViewSet, PlaylistViewSet

urlpatterns = [
    path(
        "playlists/meta",
        PlaylistMetaViewSet.as_view({"get": "list"}),
        name="browser__playlists-meta",
    ),
    path(
        "playlists/<str:playlist_pk>",
        PlaylistViewSet.as_view({"put": "update", "patch": "partial_update"}),
        name="browser__playlist",
    ),
    path(
        "playlists",
        PlaylistViewSet.as_view({"get": "list", "post": "create"}),
        name="browser__playlists",
    ),
]
