from django.test import TestCase

from api.libs.responses import LastPlayed
from api.models.users import AppUser
from api.services.spotify import SpotifyAuthService, SpotifyDataService


class SpotifyResponsesTestCase(TestCase):
    def setUp(self) -> None:
        self.user = AppUser.objects.get(is_staff=True)
        self.service = SpotifyDataService()

        self.auth_service = SpotifyAuthService()

        success, user = self.auth_service.refresh_access_token(self.user.refresh_token)

        if not success:
            raise Exception("Failed to refresh access token.")

        self.user = user or self.user

    def test_deserialize_last_played(self) -> None:
        r = self.service.last_played(self.user)

        last_played = LastPlayed.from_json(r)

        self.assertIsInstance(last_played, LastPlayed)
        self.assertIsNotNone(last_played.album_name)
