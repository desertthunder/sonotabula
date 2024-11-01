"""Browser URL configuration."""

from django.urls import path

from browser.views import PlaylistViewSet

urlpatterns = [
    path(
        "playlists", PlaylistViewSet.as_view({"get": "list"}), name="browser-playlists"
    )
]
