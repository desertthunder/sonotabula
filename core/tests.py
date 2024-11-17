import unittest
from http import HTTPStatus
from unittest.mock import MagicMock, patch

from django.test import TestCase
from django.urls import reverse
from loguru import logger

from api.libs.helpers import SpotifyAuthServiceMock, TestHelpers
from api.services.spotify import SpotifyAuthService
from core.serializers import TokenSerializer

logger.remove(0)


class CoreAuthViewTestCase(TestCase):
    def setUp(self):
        self.user = TestHelpers.create_test_user()

        self.jwt = TokenSerializer.from_user(user=self.user).encode()

    @patch.object(SpotifyAuthService, "fetch_user")
    @patch.object(SpotifyAuthService, "get_current_user")
    @patch.object(SpotifyAuthService, "get_access_token")
    def test_api_callback_view(
        self,
        mock_get_access_token: MagicMock,
        mock_get_current_user: MagicMock,
        mock_fetch_user: MagicMock,
    ):
        mock_fetch_user.return_value = SpotifyAuthServiceMock.get_full_profile()
        mock_get_access_token.return_value = SpotifyAuthServiceMock.get_access_token()
        mock_get_current_user.return_value = SpotifyAuthServiceMock.get_current_user()
        path = reverse("api_callback")
        response = self.client.get(path, QUERY_STRING="code=FAKE_CODE&state=app-login")

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    @patch.object(SpotifyAuthService, "build_redirect_uri")
    def test_redirect_url_view(self, mock_build_redirect_url: MagicMock):
        fake_redirect_url = "http://local.dashspot.dev/redirect"
        mock_build_redirect_url.return_value = (
            SpotifyAuthServiceMock.build_redirect_url(
                url=fake_redirect_url,
            )
        )

        path = reverse("redirect_uri")
        response = self.client.post(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json(), {"redirect": fake_redirect_url})

    @patch.object(SpotifyAuthService, "refresh_access_token")
    def test_refresh_token_view(self, mock_refresh_access_token: MagicMock):
        mock_refresh_access_token.return_value = (
            SpotifyAuthServiceMock.refresh_access_token(user=self.user)
        )

        path = reverse("refresh_token")
        response = self.client.put(
            path, headers={"Authorization": f"Bearer {self.jwt}"}
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)


class AppUserManagerTestCase(TestCase):
    """AppUserManager test case."""

    @unittest.skip("TODO")
    def test_from_spotify(self) -> None:
        """Test from_spotify method."""
        pass


class AppUserTestCase(TestCase):
    """AppUser model tests."""

    @unittest.skip("TODO")
    def test_str(self) -> None:
        """Test __str__ method."""
        pass

    @unittest.skip("TODO")
    def test_should_update(self) -> None:
        """Test should_update method."""
        pass

    @unittest.skip("TODO")
    def test_update_token_set(self) -> None:
        """Test update_token_set method."""
        pass

    @unittest.skip("Not implemented")
    def test_should_refresh_token(self) -> None:
        """Test should_refresh_token method."""
        pass
