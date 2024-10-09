"""API Routing."""

from django.urls import path

from api.views import (
    LastPlayedView,
    LibraryAlbumsView,
    LibraryArtistsView,
    LibraryPlaylistsView,
    LibraryTracksView,
    LoginView,
    RecentlyPlayedView,
    ValidateView,
)

urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
    path("validate", ValidateView.as_view(), name="validate-token"),
    path("playback/last", LastPlayedView.as_view(), name="last-played"),
    path("playback/recent", RecentlyPlayedView.as_view(), name="recently-played"),
    path("library/playlists", LibraryPlaylistsView.as_view(), name="library-playlists"),
    path("library/albums", LibraryAlbumsView.as_view(), name="library-albums"),
    path("library/artists", LibraryArtistsView.as_view(), name="library-artists"),
    path("library/tracks", LibraryTracksView.as_view(), name="library-tracks"),
]
