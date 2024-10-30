import logging
import random

from django.test import TestCase
from django.urls import reverse

from api.models.analysis import Analysis
from api.models.permissions import Token
from api.services.spotify import SpotifyAuthService
from core.models import AppUser

logging.disable(logging.ERROR)


class PlaybackViewTestCase(TestCase):
    def setUp(self) -> None:
        self.auth_service = SpotifyAuthService()
        self.user = AppUser.objects.get(is_staff=True)

        user = self.auth_service.refresh_access_token(self.user.refresh_token)

        self.user = user or self.user
        self.jwt = Token(self.user).encode()

    def test_last_played_view(self):
        path = reverse("last-played")

        response = self.client.get(
            path, headers={"Authorization": f"Bearer {self.jwt}"}
        )

        data = response.json().get("data")

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(data)
        self.assertIn("track_name", data)

    def test_recently_played_view(self):
        path = reverse("recently-played")
        path = f"{path}?limit=2"

        response = self.client.get(
            path, headers={"Authorization": f"Bearer {self.jwt}"}
        )
        data = response.json().get("data")

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(data)
        self.assertEqual(len(data), 2)


class LibraryViewTestCase(TestCase):
    def setUp(self) -> None:
        self.auth_service = SpotifyAuthService()
        self.user = AppUser.objects.get(is_staff=True)

        user = self.auth_service.refresh_access_token(self.user.refresh_token)

        self.user = user or self.user
        self.jwt = Token(self.user).encode()

    def test_library_playlists_view(self):
        path = reverse("library-playlists")
        path = f"{path}?limit=2"

        response = self.client.get(
            path, headers={"Authorization": f"Bearer {self.jwt}"}
        )

        data = response.json().get("data")

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(data)
        self.assertEqual(len(data), 2)

    def test_library_albums_view(self):
        path = reverse("library-albums")
        path = f"{path}?limit=2"

        response = self.client.get(
            path, headers={"Authorization": f"Bearer {self.jwt}"}
        )

        data = response.json().get("data")

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(data)
        self.assertEqual(len(data), 2)

    def test_library_artist_view(self):
        path = reverse("library-artists")
        path = f"{path}?limit=2"

        response = self.client.get(
            path, headers={"Authorization": f"Bearer {self.jwt}"}
        )

        data = response.json().get("data")

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(data)
        self.assertEqual(len(data), 2)

    def test_library_tracks_view(self):
        path = reverse("library-tracks")
        path = f"{path}?limit=2"

        response = self.client.get(
            path, headers={"Authorization": f"Bearer {self.jwt}"}
        )

        data = response.json().get("data")

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(data)
        self.assertEqual(len(data), 2)


class AuthViewTestCase(TestCase):
    def test_login_view(self):
        pass

    def test_validate_view(self):
        pass


class AnalysisViewTestCase(TestCase):
    def test_analysis_view(self):
        pass


class BrowserPlaylistViewTestCase(TestCase):
    def setUp(self) -> None:
        self.auth_service = SpotifyAuthService()
        self.user = AppUser.objects.get(is_staff=True)
        self.jwt = Token(self.user).encode()

    def test_browser_playlist_view(self):
        path = reverse("list-browser-playlists")

        response = self.client.get(
            path, headers={"Authorization": f"Bearer {self.jwt}"}
        )

        data = response.json().get("data")

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(data)
        self.assertGreater(len(data), 0)

    def filter_by_name(self):
        path = reverse("list-browser-playlists")
        path = f"{path}?name=random"

        response = self.client.get(
            path, headers={"Authorization": f"Bearer {self.jwt}"}
        )

        data = response.json().get("data")

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(data)
        self.assertGreater(len(data), 0)


class BrowserPlaylistTracksViewTestCase(TestCase):
    def setUp(self) -> None:
        self.auth_service = SpotifyAuthService()
        self.user = AppUser.objects.get(is_staff=True)
        self.analysis = Analysis.objects.prefetch_related("playlist").first()

        if self.analysis is None:
            self.fail("No analysis found.")

        self.playlist = self.analysis.playlist
        self.jwt = Token(self.user).encode()

    def test_browser_playlist_tracks_view(self):
        path = reverse(
            "list-browser-playlist-tracks",
            kwargs={"playlist_id": str(self.playlist.id)},
        )

        response = self.client.get(
            path, headers={"Authorization": f"Bearer {self.jwt}"}
        )

        data = response.json().get("data")
        track = random.choice(data)

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(data)
        self.assertGreater(len(data), 0)
        self.assertIn("name", track)
        self.assertIn("features", track)
