"""API Routing."""

from django.urls import path

from api.views import LastPlayedView, LoginView, RecentlyPlayedView, ValidateView

urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
    path("validate", ValidateView.as_view(), name="validate-token"),
    path("playback/last", LastPlayedView.as_view(), name="last-played"),
    path("playback/recent", RecentlyPlayedView.as_view(), name="recently-played"),
]
