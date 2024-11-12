"""API Routing."""

from django.urls import include, path

urlpatterns = [
    path("v1/playback/", include("apps.urls")),
    path("v1/browser/", include("browser.urls")),
    path("v1/library/", include("library.urls")),
    path("v1/user/", include("core.urls")),
]
