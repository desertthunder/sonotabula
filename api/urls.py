"""API Routing."""

from django.urls import include, path

from api.views import auth, browser, data
from core.views import ProfileViewSet

urlpatterns = [
    # TODO: Move to core
    path("login", auth.LoginView.as_view(), name="login"),
    # TODO: Move to core
    path("validate", auth.ValidateView.as_view(), name="validate-token"),
    # TODO: Move to core (see below)
    path("data/saved", data.UserSavedItemsView.as_view(), name="user-saved-items"),
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
    path("playback/", include("apps.urls")),
    path("v1/library/", include("library.urls")),
    # TODO: Implement
    # path("v1/profile/saved", ProfileViewSet.as_view({"get": "list"}), \
    # name="profile-saved"),
    # TODO: Move to core
    path("v1/profile", ProfileViewSet.as_view({"get": "retrieve"}), name="profile"),
]
