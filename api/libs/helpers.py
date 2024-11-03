"""Helper functions for tests."""

import datetime
import json

import httpx
from django.utils import timezone

from api.libs.requests import RedirectURI
from api.serializers.authentication import AccessToken, CurrentUser
from core.models import AppUser


def open_fixture_file(file_path: str) -> str:
    """Open a fixture file and return it as a json string."""
    file_path = f"api/libs/fixtures/{file_path}"
    with open(file_path) as file:
        return json.load(file)


# Spotify Auth Service Mocks
class SpotifyAuthServiceMock:
    """Collection of method decorators mocking the SpotifyAuthService class."""

    @classmethod
    def auth(cls: type["SpotifyAuthServiceMock"]) -> httpx.BasicAuth:
        """Mock the auth method's return value."""
        return httpx.BasicAuth(
            "FAKE_CLIENT_ID",
            "FAKE_CLIENT_SECRET",
        )

    @classmethod
    def get_access_token(cls: type["SpotifyAuthServiceMock"]) -> AccessToken:
        """Mock the get_access_token method."""
        return AccessToken(
            access_token="FAKE_ACCESS_TOKEN",  # noqa: S106
            refresh_token="FAKE_REFRESH_TOKEN",  # noqa: S106
            token_type="Bearer",  # noqa: S106
            token_expiry=timezone.now() + datetime.timedelta(seconds=3600),
        )

    @classmethod
    def refresh_access_token(
        cls: type["SpotifyAuthServiceMock"], user: AppUser
    ) -> AppUser:
        """Mock the refresh_access_token method."""
        return user

    @classmethod
    def get_current_user(cls: type["SpotifyAuthServiceMock"]) -> CurrentUser:
        """Mock the get_current_user method."""
        return CurrentUser(
            display_name="FAKE_DISPLAY_NAME", email="FAKE_EMAIL", id="FAKE_ID"
        )

    @classmethod
    def get_full_profile(cls: type["SpotifyAuthServiceMock"]) -> dict:
        """Mock the get_full_profile method."""
        json_str = open_fixture_file("auth__get_full_profile.json")
        return json.loads(json_str)

    @classmethod
    def build_redirect_url(
        cls: type["SpotifyAuthServiceMock"], url: str = "https://google.com"
    ) -> str:
        """Mock the build_redirect_url method."""
        return RedirectURI(
            _url=httpx.URL(url),
        ).as_str


# Spotify Data Service Mocks

# Spotify Library Service Mocks

# Spotify Playback Service Mocks
