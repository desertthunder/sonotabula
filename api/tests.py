"""API Package/app Tests."""

import logging
import random
import time

from django.test import TestCase
from django.urls import reverse

from api.models.permissions import Token
from api.models.users import AppUser
from api.services.spotify import SpotifyAuthService, SpotifyDataService

logging.disable(logging.ERROR)


class APIAnalysisViewTestCase(TestCase):
    def setUp(self) -> None:
        self.user = AppUser.objects.get(is_staff=True)
        self.auth_service = SpotifyAuthService()
        self.data_service = SpotifyDataService()

        if self.user.token_expired:
            success, user = self.auth_service.refresh_access_token(
                self.user.refresh_token
            )

            if not success:
                raise Exception("Failed to refresh access token.")

            if user:
                self.user = user

        self.jwt = Token(self.user).encode()
        self.playlist_id = self.data_service.library_playlists(self.user, 1)[0]["id"]

    def test_playlist_analysis_view(self):
        url = reverse("playlist-analysis", kwargs={"playlist_id": self.playlist_id})
        time.sleep(0.5)
        r = self.client.get(url, headers={"Authorization": f"Bearer {self.jwt}"})

        self.assertEqual(r.status_code, 200)
        self.assertIn("version", r.json())
        self.assertIn("owner", r.json())
        self.assertIn("tracks", r.json())


class APILibraryViewTestCase(TestCase):
    def setUp(self) -> None:
        self.user = AppUser.objects.get(is_staff=True)
        self.auth_service = SpotifyAuthService()

        if self.user.token_expired:
            success, user = self.auth_service.refresh_access_token(
                self.user.refresh_token
            )

            if not success:
                raise Exception("Failed to refresh access token.")

            if user:
                self.user = user

        self.jwt = Token(self.user).encode()

    def test_limit_param(self):
        limit = random.randint(1, 10)
        view_name = random.choice(
            [
                "library-playlists",
                "library-artists",
                "library-albums",
                "library-tracks",
            ]
        )
        url = reverse(view_name) + f"?limit={limit}"
        r = self.client.get(url, headers={"Authorization": f"Bearer {self.jwt}"})
        data = r.json().get("data")

        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "data")
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), limit)

    def test_library_playlists_view(self):
        url = reverse("library-playlists")
        r = self.client.get(url, headers={"Authorization": f"Bearer {self.jwt}"})
        data = r.json().get("data")

        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "data")
        self.assertIsInstance(data, list)
        self.assertIn("spotify_id", data[0])

    def test_library_artists_view(self):
        url = reverse("library-artists")
        r = self.client.get(url, headers={"Authorization": f"Bearer {self.jwt}"})
        data = r.json().get("data")

        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "data")
        self.assertIsInstance(data, list)
        self.assertIn("spotify_id", data[0])

    def test_library_albums_view(self):
        url = reverse("library-albums")
        r = self.client.get(url, headers={"Authorization": f"Bearer {self.jwt}"})
        data = r.json().get("data")

        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "data")
        self.assertIsInstance(data, list)
        self.assertIn("spotify_id", data[0])

    def test_library_tracks_view(self):
        url = reverse("library-tracks")
        r = self.client.get(url, headers={"Authorization": f"Bearer {self.jwt}"})
        data = r.json().get("data")

        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "data")
        self.assertIsInstance(data, list)
        self.assertIn("spotify_id", data[0])
