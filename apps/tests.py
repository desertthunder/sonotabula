import logging
from unittest import mock

from django.test import TestCase
from django.urls import reverse

from api.libs.helpers import (
    SpotifyPlaybackServiceMock,
    TestHelpers,
)
from api.models import Album, Artist, Track
from api.services.spotify import (
    SpotifyPlaybackService,
)
from apps.models import ListeningHistory
from core.serializers import TokenSerializer

logging.disable(logging.ERROR)


class ListeningHistoryViewTestCase(TestCase):
    def setUp(self):
        self.user = TestHelpers.create_test_user()

        self.jwt = TokenSerializer.from_user(user=self.user).encode()

    @mock.patch.object(SpotifyPlaybackService, "recently_played")
    def test_get_recently_played(self, mock_get_recently_played: mock.MagicMock):
        mock_get_recently_played.return_value = (
            SpotifyPlaybackServiceMock.recently_played()
        )

        response = self.client.get(
            reverse("listening-history"),
            headers={"Authorization": f"Bearer {self.jwt}"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("id", response.json().get("data"))
        self.assertEqual(ListeningHistory.objects.count(), 10)
        self.assertGreaterEqual(Track.objects.count(), 1)
        self.assertGreaterEqual(Artist.objects.count(), 1)
        self.assertGreaterEqual(Album.objects.count(), 1)
