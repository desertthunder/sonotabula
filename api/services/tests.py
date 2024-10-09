"""Spotify Service tests."""

import collections
import logging
import time
from secrets import randbelow
from unittest import skip

from django.test import TestCase

from api.models.users import AppUser
from api.services.spotify import (
    SpotifyAnalysisService,
    SpotifyAuthService,
    SpotifyDataService,
)
from api.services.spotify.analysis import Playlist as ExpandedPlaylist

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


class SpotifyAnalysisServiceTestCase(TestCase):
    def setUp(self) -> None:
        self.user = AppUser.objects.get(is_staff=True)
        self.service = SpotifyAnalysisService()

        self.auth_service = SpotifyAuthService()
        self.data_service = SpotifyDataService()

        success, user = self.auth_service.refresh_access_token(self.user.refresh_token)

        if not success:
            raise Exception("Failed to refresh access token.")

        if user:
            self.user = user

        self.playlist = self.data_service.library_playlists(self.user, 1)[0]
        self.playlist_id = self.playlist["id"]

    @skip("Skipping due to rate limiting.")
    def test_get_playlist(self) -> None:
        r = self.service.get_playlist(self.playlist_id, self.user)

        self.assertIn("id", r)
        self.assertEqual(r["id"], self.playlist["id"])

        time.sleep(1)

    @skip("Skipping due to rate limiting.")
    def test_get_playlist_tracks(self) -> None:
        r = self.service.get_playlist_tracks(self.playlist_id, self.user)

        self.assertIsInstance(r, collections.abc.Iterable)

        time.sleep(1)

    @skip("Skipping due to rate limiting.")
    def test_get_artist(self) -> None:
        track = self.data_service.last_played(self.user)[0]
        self.assertIsNotNone(track)

        artists = track.get("track", {}).get("artists", [{}])
        self.assertIsNot(len(artists), 0)

        r = self.service.get_artist(artists[0]["id"], self.user)

        self.assertIn("id", r)
        self.assertIn("name", r)

        time.sleep(1)

    @skip("Skipping due to rate limiting.")
    def test_get_audio_features(self) -> None:
        track = self.data_service.last_played(self.user)[0]
        self.assertIsNotNone(track)

        r = self.service.get_track_features(track["id"], self.user)

        self.assertIn("id", r)
        self.assertIn("danceability", r)

        time.sleep(1)

    def test_expand_playlist(self) -> None:
        r = self.service.expand_playlist(self.playlist_id, self.user)

        self.assertIsInstance(r, ExpandedPlaylist)
