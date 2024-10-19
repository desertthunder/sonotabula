"""API Routing."""

from django.urls import path

from api.views import auth, browser, data, library, playback

urlpatterns = [
    path("login", auth.LoginView.as_view(), name="login"),
    path("validate", auth.ValidateView.as_view(), name="validate-token"),
    path("data/saved", data.UserSavedItemsView.as_view(), name="user-saved-items"),
    path("playback/last", playback.LastPlayedView.as_view(), name="last-played"),
    path(
        "playback/recent", playback.RecentlyPlayedView.as_view(), name="recently-played"
    ),
    path("library/playlists/<str:playlist_id>", library.LibraryPlaylistsView.as_view()),
    path(
        "library/playlists",
        library.LibraryPlaylistsView.as_view(),
        name="library-playlists",
    ),
    path("library/albums", library.LibraryAlbumsView.as_view(), name="library-albums"),
    path(
        "library/artists", library.LibraryArtistsView.as_view(), name="library-artists"
    ),
    path("library/tracks", library.LibraryTracksView.as_view(), name="library-tracks"),
    path(
        "browser/playlist/<str:playlist_id>/tracks",
        browser.BrowserPlaylistView.as_view(),
        name="get-browser-playlist",
    ),
    path(
        "browser/playlists",
        browser.BrowserPlaylistListView.as_view(),
        name="list-browser-playlists",
    ),
    path(
        "browser/albums",
        browser.BrowserAlbumListView.as_view(),
        name="list-browser-albums",
    ),
    path(
        "browser/tracks",
        browser.BrowserTrackListView.as_view(),
        name="list-browser-tracks",
    ),
]
