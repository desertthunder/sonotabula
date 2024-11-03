from http import HTTPStatus
from unittest.mock import MagicMock, patch

from django.test import TestCase
from loguru import logger

from api.libs.helpers import SpotifyAuthServiceMock
from api.models.permissions import Token
from api.services.spotify.auth import SpotifyAuthService
from core.models import AppUser

logger.remove(0)


class AuthViewTestCase(TestCase):
    def setUp(self):
        self.user = AppUser.objects.from_spotify(
            SpotifyAuthServiceMock.get_current_user(),
            SpotifyAuthServiceMock.get_access_token(),
        )

        self.jwt = Token(user=self.user).encode()

    @patch.object(SpotifyAuthService, "get_current_user")
    @patch.object(SpotifyAuthService, "get_access_token")
    def test_get_login_view(
        self, mock_get_access_token: MagicMock, mock_get_current_user: MagicMock
    ):
        mock_get_access_token.return_value = SpotifyAuthServiceMock.get_access_token()
        mock_get_current_user.return_value = SpotifyAuthServiceMock.get_current_user()

        response = self.client.get(
            "/api/login", QUERY_STRING="code=FAKE_CODE&state=app-login"
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    @patch.object(SpotifyAuthService, "build_redirect_uri")
    def test_post_login_view(self, mock_build_redirect_url: MagicMock):
        fake_redirect_url = "http://local.dashspot.dev/redirect"
        mock_build_redirect_url.return_value = (
            SpotifyAuthServiceMock.build_redirect_url(
                url=fake_redirect_url,
            )
        )

        response = self.client.post("/api/login")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json(), {"redirect": fake_redirect_url})

    @patch.object(SpotifyAuthService, "refresh_access_token")
    def test_post_validate_view(self, mock_refresh_access_token: MagicMock):
        mock_refresh_access_token.return_value = (
            SpotifyAuthServiceMock.refresh_access_token(user=self.user)
        )

        response = self.client.post(
            "/api/validate", headers={"Authorization": f"Bearer {self.jwt}"}
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
