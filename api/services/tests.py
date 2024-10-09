"""Spotify Service tests."""

import logging
import time
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

        time.sleep(1)

    def test_get_recently_played(self) -> None:
        r = self.service.recently_played(self.user, 2)

        self.assertIsInstance(r, list)
        self.assertEqual(len(r), 2)
        self.assertIsInstance(r[randbelow(len(r))], dict)

        time.sleep(1)

    def test_get_library_playlists(self) -> None:
        r = self.service.library_playlists(self.user, 2)

        self.assertIn("type", r[0])
        self.assertEqual(r[0]["type"], "playlist")
        self.assertIsInstance(r, list)
        self.assertEqual(len(r), 2)
        self.assertIsInstance(r[randbelow(len(r))], dict)

        time.sleep(1)

    def test_get_library_artists(self) -> None:
        r = self.service.library_artists(self.user, 2)

        self.assertIn("type", r[0])
        self.assertEqual(r[0]["type"], "artist")
        self.assertIsInstance(r, list)
        self.assertEqual(len(r), 2)
        self.assertIsInstance(r[randbelow(len(r))], dict)

        time.sleep(1)

    def test_get_library_albums(self) -> None:
        r = self.service.library_albums(self.user, 2)

        self.assertIn("album", r[0])
        self.assertIsInstance(r, list)
        self.assertEqual(len(r), 2)
        self.assertIsInstance(r[randbelow(len(r))], dict)

        time.sleep(1)
