import unittest

from django.test import TestCase
from faker import Faker

from api.models.playlist import Playlist, SyncPlaylist
from api.models.users import AppUser

faker = Faker()


class UserManagerTestCase(TestCase):
    @unittest.skip("Not implemented")
    def test_create_user_from_spotify(self):
        pass


class UserModelTestCase(TestCase):
    @unittest.skip("Not implemented")
    def test_token_expired_property(self):
        pass

    @unittest.skip("Not implemented")
    def test_update_token_set_method(self):
        pass


class PlaylistSyncManagerTestCase(TestCase):
    def setUp(self):
        self.playlists = [
            SyncPlaylist(
                name=faker.name(), spotify_id=faker.uuid4(), owner_id=faker.uuid4()
            )
            for _ in range(3)
        ]

        self.user = AppUser.objects.get(is_staff=True)

    def test_create_to_sync(self):
        initial_count = Playlist.sync.count()

        result = Playlist.sync.create_to_sync(self.playlists, self.user.pk)

        for pk, spotify_id in result:
            self.assertTrue(Playlist.sync.filter(pk=pk, spotify_id=spotify_id).exists())

        self.assertEqual(Playlist.sync.count(), initial_count + 3)
