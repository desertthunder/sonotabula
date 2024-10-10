"""Spotify Service tests."""

import logging
from unittest import skip

from django.test import TestCase

logging.disable(logging.ERROR)


class SpotifyAuthServiceTestCase(TestCase):
    """Spotify Auth Service tests."""

    @skip("Not implemented")
    def test_build_redirect_uri(self):
        pass

    @skip("Not implemented")
    def test_refresh_access_token(self):
        pass

    @skip("Not implemented")
    def test_get_current_user(self):
        pass
