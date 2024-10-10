"""Spotify Service tests."""

import logging

from django.test import TestCase
from django.test.testcases import SerializeMixin

from api.models.users import AppUser
from api.serializers.authentication import CurrentUser
from api.services.spotify import SpotifyAuthService

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
