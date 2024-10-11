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
        # self.playlists = [
        #     SyncPlaylist(
        #         name=faker.name(), spotify_id=faker.uuid4(), owner_id=faker.uuid4()
        #     )
        #     for _ in range(3)
        # ]
        self.data = [
            {
                "name": faker.name(),
                "id": faker.uuid4(),
                "owner": {"id": faker.uuid4()},
                "snapshot_id": faker.uuid4(),
                "images": [{"url": faker.url()}],
                "public": faker.boolean(),
                "collaborative": faker.boolean(),
                "description": faker.text(),
            }
            for _ in range(faker.random_int(min=1, max=4))
        ]

        self.user = AppUser.objects.get(is_staff=True)

    def test_validate_iterator(self):
        result = Playlist.sync.before_sync(self.data)

        for playlist in result:
            self.assertIsInstance(playlist, SyncPlaylist)

    def test_sync(self):
        initial_count = Playlist.objects.count()
        data = Playlist.sync.before_sync(self.data)

        # TODO: change the name of the method to `call_sync`
        result = Playlist.sync.sync(playlists=data, user_pk=self.user.pk)

        for playlist_pk, _ in result:
            self.assertIsNotNone(playlist_pk)

        self.assertEqual(Playlist.objects.count(), initial_count + len(self.data))
