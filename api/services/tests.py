"""Spotify Service tests."""

import logging
import typing

from django.test import TestCase
from django.test.testcases import SerializeMixin

from api.models.users import AppUser
from api.serializers.authentication import CurrentUser
from api.services.spotify import SpotifyAuthService, SpotifyPlaybackService

logging.disable(logging.ERROR)


class SpotifyAuthServiceTestCase(SerializeMixin, TestCase):
    """Spotify Auth Service tests."""

    lockfile = __file__

    def setUp(self):
        self.service = SpotifyAuthService()
        self.user = AppUser.objects.get(is_staff=True)

    def test_build_redirect_uri(self):
        uri = self.service.build_redirect_uri()

        self.assertIsNotNone(uri)
        self.assertIn("state=app-login", uri)
        self.assertIn("client_id=", uri)
        self.assertIn("redirect_uri=", uri)
        self.assertIn("scope=", uri)

    def test_refresh_access_token(self):
        original_access_token = self.user.access_token
        status, user = self.service.refresh_access_token(self.user.refresh_token)

        self.assertTrue(status)
        self.assertIsNotNone(user)
        self.assertNotEqual(original_access_token, user.access_token)

    def test_get_current_user(self):
        _, user = self.service.refresh_access_token(self.user.refresh_token)
        data = self.service.get_current_user(user.access_token)

        self.assertIsNotNone(data)
        self.assertIsInstance(data, CurrentUser)
        self.assertEqual(data.id, self.user.spotify_id)


class SpotifyPlaybackServiceTestCase(TestCase):
    def setUp(self):
        self.service = SpotifyPlaybackService()
        self.auth_service = SpotifyAuthService()

        user_refresh_token = AppUser.objects.values_list(
            "refresh_token", flat=True
        ).first()

        _, self.user = self.auth_service.refresh_access_token(user_refresh_token)

    def test_recently_played(self):
        data = self.service.recently_played(self.user, items=2)

        self.assertIsNotNone(data)
        self.assertIsInstance(data, typing.Iterable)
        self.assertEqual(len(list(data)), 2)

    def test_now_playing(self):
        self.assertRaises(NotImplementedError, self.service.now_playing)
