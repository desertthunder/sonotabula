"""Core URL patterns and configuration."""

from django.urls import path

from core.views import AuthenticationViewSet, ProfileViewSet

urlpatterns = [
    path(
        "auth/refresh",
        AuthenticationViewSet.as_view({"put": "update"}),
        name="refresh_token",
    ),
    path(
        "auth/callback",
        AuthenticationViewSet.as_view({"get": "api_callback"}),
        name="api_callback",
    ),
    path(
        "auth/",
        AuthenticationViewSet.as_view({"post": "create"}),
        name="redirect_uri",
    ),
    path("profile/", ProfileViewSet.as_view({"get": "retrieve"}), name="profile"),
]
