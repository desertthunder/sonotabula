"""Spotify Service tests."""

import logging
from secrets import randbelow

from django.test import TestCase

from api.models.users import AppUser
from api.services.spotify import SpotifyAuthService, SpotifyDataService

logging.disable(logging.ERROR)


class SpotifyDataServiceTestCase(TestCase):
    def setUp(self) -> None:
        self.user = AppUser.objects.get(is_staff=True)
        self.service = SpotifyDataService()

        self.auth_service = SpotifyAuthService()

        success, user = self.auth_service.refresh_access_token(self.user.refresh_token)

        if not success:
            raise Exception("Failed to refresh access token.")

        if user:
            self.user = user

    def test_get_last_played(self) -> None:
        r = self.service.last_played(self.user)

        self.assertIsInstance(r, list)
        self.assertEqual(len(r), 1)
        self.assertIsInstance(r[randbelow(len(r))], dict)

    def test_get_recently_played(self) -> None:
        r = self.service.recently_played(self.user, 2)

        self.assertIsInstance(r, list)
        self.assertEqual(len(r), 2)
        self.assertIsInstance(r[randbelow(len(r))], dict)
