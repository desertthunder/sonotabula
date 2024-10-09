import collections
import collections.abc
import time

from django.test import TestCase

from api.libs.responses import (
    Album,
    Artist,
    Playlist,
    RecentlyPlayed,
    Track,
)
from api.models.users import AppUser
from api.services.spotify import SpotifyAuthService, SpotifyDataService


class SpotifyResponsesTestCase(TestCase):
    def setUp(self) -> None:
        self.user = AppUser.objects.get(is_staff=True)
        self.service = SpotifyDataService()

        self.auth_service = SpotifyAuthService()

        if self.user.token_expired:
            success, user = self.auth_service.refresh_access_token(
                self.user.refresh_token
            )

            if not success:
                raise Exception("Failed to refresh access token.")

            self.user = user or self.user

    def test_deserialize_recently_played(self) -> None:
        r = self.service.recently_played(self.user, 2)

        iter = RecentlyPlayed.list(r)
        last_played = list(iter)

        self.assertIsInstance(iter, collections.abc.Iterable)
        self.assertIsInstance(last_played, list)
        self.assertEqual(len(last_played), 2)

        time.sleep(1)

    def test_deserialize_playlists(self) -> None:
        r = self.service.library_playlists(self.user, 2)

        iter = Playlist.list(r)

        playlists = list(iter)
        playlist = Playlist.get(r[0])

        self.assertIsInstance(iter, collections.abc.Iterable)
        self.assertIsInstance(playlists, list)
        self.assertEqual(len(playlists), 2)
        self.assertIsInstance(playlist, Playlist)

        time.sleep(1)

    def test_deserialize_albums(self) -> None:
        r = self.service.library_albums(self.user, 2)

        iter = Album.list(r)

        albums = list(iter)
        album = Album.get(r[0])

        self.assertIsInstance(iter, collections.abc.Iterable)
        self.assertIsInstance(albums, list)
        self.assertEqual(len(albums), 2)
        self.assertIsInstance(album, Album)

        time.sleep(1)

    def test_deserialize_tracks(self) -> None:
        r = self.service.library_tracks(self.user, 2)
        iter = Track.list(r)

        tracks = list(iter)
        track = Track.get(r[0])

        self.assertIsInstance(iter, collections.abc.Iterable)
        self.assertIsInstance(tracks, list)
        self.assertEqual(len(tracks), 2)
        self.assertIsInstance(track, Track)

        time.sleep(1)

    def test_deserialize_artists(self) -> None:
        r = self.service.library_artists(self.user, 2)

        iter = Artist.list(r)

        artists = list(iter)
        artist = Artist.get(r[0])

        self.assertIsInstance(iter, collections.abc.Iterable)
        self.assertIsInstance(artists, list)
        self.assertEqual(len(artists), 2)
        self.assertIsInstance(artist, Artist)

        time.sleep(1)
