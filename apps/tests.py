import logging

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from api.models.permissions import Token
from api.services.spotify import SpotifyAuthService, SpotifyPlaybackService

auth_service = SpotifyAuthService()
playback_service = SpotifyPlaybackService()

User = get_user_model()

logging.disable(logging.ERROR)


class ListeningHistoryViewTestCase(TestCase):
    """Listening history view test case."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.user = User.objects.get(is_staff=True)
        self.service = playback_service
        self.auth = auth_service

        self.jwt = Token(self.user)

    def test_get_most_recent(self) -> None:
        """Test get request to api/playback/recent."""
        path = reverse("listening-history")

        resp = self.client.get(
            path, headers={"Authorization": f"Bearer {self.jwt.encode()}"}
        )

        self.assertEqual(resp.status_code, 200)

    def test_get_small_batch(self) -> None:
        """Test getting a small batch of tracks."""
        path = reverse("listening-history")

        resp = self.client.put(
            path, headers={"Authorization": f"Bearer {self.jwt.encode()}"}
        )

        self.assertEqual(resp.status_code, 200)

    def test_get_large_batch(self) -> None:
        """Test getting a large batch of tracks."""
        path = reverse("listening-history")

        resp = self.client.post(
            f"{path}?limit=10", headers={"Authorization": f"Bearer {self.jwt.encode()}"}
        )

        self.assertEqual(resp.status_code, 200)
