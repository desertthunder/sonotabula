"""Browser URL configuration."""

from django.urls import path

from browser.views import (
    AlbumMetaViewSet,
    AlbumViewSet,
    PlaylistMetaViewSet,
    PlaylistViewSet,
)

urlpatterns = [
    path(
        "playlists/meta",
        PlaylistMetaViewSet.as_view({"get": "list"}),
        name="browser__playlists-meta",
    ),
    path(
        "playlists/<str:playlist_pk>",
        PlaylistViewSet.as_view(
            {"put": "update", "patch": "partial_update", "get": "retrieve"}
        ),
        name="browser__playlist",
    ),
    path(
        "playlists",
        PlaylistViewSet.as_view({"get": "list", "post": "create"}),
        name="browser__playlists",
    ),
    path(
        "albums/meta",
        AlbumMetaViewSet.as_view({"get": "list"}),
        name="browser__albums-meta",
    ),
    path(
        "albums/<str:album_pk>",
        AlbumViewSet.as_view({"get": "retrieve"}),
        name="browser__album",
    ),
    path("albums", AlbumViewSet.as_view({"get": "list"}), name="browser__albums"),
]
