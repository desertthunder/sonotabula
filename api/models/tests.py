import json
import unittest

from django.test import TestCase
from faker import Faker

from api.libs.helpers import TestHelpers
from api.models.analysis import Analysis
from api.models.music import Album, Artist
from api.models.playlist import Playlist
from api.models.track import Track
from api.serializers.validation.playlist import SyncPlaylist
from api.serializers.validation.track import SyncTrackData

faker = Faker()


@unittest.skip("Not implemented")
class UserManagerTestCase(TestCase):
    @unittest.skip("Not implemented")
    def test_create_user_from_spotify(self):
        pass


@unittest.skip("Not implemented")
class UserModelTestCase(TestCase):
    @unittest.skip("Not implemented")
    def test_token_expired_property(self):
        pass

    @unittest.skip("Not implemented")
    def test_update_token_set_method(self):
        pass


class PlaylistSyncManagerTestCase(TestCase):
    def setUp(self):
        # Example:
        #
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

        self.user = TestHelpers.create_test_user()
        self.library = self.user.library

    def test_validate_iterator(self):
        result = Playlist.sync.pre_sync(self.data)
        self.assertIsNotNone(result)

        for playlist in result:
            self.assertIsInstance(playlist, SyncPlaylist)
            self.assertIsNotNone(playlist.spotify_id)

    def test_sync(self):
        initial_count = Playlist.objects.count()
        data = Playlist.sync.pre_sync(self.data)
        results = Playlist.sync.do(playlists=data, user_pk=self.user.pk)

        self.assertIsNotNone(results)
        self.assertGreater(len(results), 0)
        self.assertEqual(Playlist.objects.count(), initial_count + len(self.data))

    def test_complete(self):
        data = Playlist.sync.pre_sync(self.data)
        playlists = Playlist.sync.do(playlists=list(data), user_pk=self.user.pk)
        result = Playlist.sync.complete_sync(self.library.pk, playlists)

        self.assertGreater(len(result), 0)
        self.assertIsNotNone(self.library)
        self.assertEqual(self.library.playlists.count(), len(self.data))


class TrackSyncManagerTestCase(TestCase):
    def setUp(self):
        with open("api/libs/fixtures/playlist-tracks.json") as f:
            self.data = json.load(f)

    def fake_iterator(self):
        yield from self.data.get("items")[:3]

    def test_before_sync(self):
        result = Track.sync.pre_sync(self.fake_iterator())

        for data in result:
            self.assertIsInstance(data, SyncTrackData)
            self.assertIsNotNone(data.track.spotify_id)
            self.assertIsNotNone(data.album.spotify_id)
            self.assertGreater(len(data.artists), 0)

    def test_sync(self):
        initial_track_count = Track.objects.count()
        initial_album_count = Album.objects.count()
        initial_artist_count = Artist.objects.count()

        data = Track.sync.pre_sync(self.fake_iterator())

        # We need to randomize the spotify ids otherwise
        # we can't properly evaluate that these were added
        for entry in data:
            entry.track.spotify_id = faker.uuid4()
            entry.album.spotify_id = faker.uuid4()

            for artist in entry.artists:
                artist.spotify_id = faker.uuid4()

        tracks_added = 0
        artists_added = 0

        for entry in data:
            artists_added += len(entry.artists)
            tracks_added += 1

        result = Track.sync.do(data)

        for track_pk, _ in result:
            self.assertIsNotNone(track_pk)

        self.assertEqual(Track.objects.count(), initial_track_count + tracks_added)
        self.assertEqual(Album.objects.count(), initial_album_count + tracks_added)
        self.assertEqual(Artist.objects.count(), initial_artist_count + artists_added)

    def test_complete(self):
        playlist = Playlist.objects.create(
            name=faker.name(), spotify_id=faker.uuid4(), owner_id=faker.uuid4()
        )

        data = Track.sync.pre_sync(self.fake_iterator())
        results = Track.sync.do(data)
        completed = Track.sync.complete_sync(playlist.pk, results)

        self.assertIsNotNone(completed)
        self.assertEqual(playlist.tracks.count(), len(results))


@unittest.skip("Not implemented")
class AnalysisManagerTestCase(TestCase):
    def setUp(self):
        self.playlist = Playlist.objects.create(
            name=faker.name(), spotify_id=faker.uuid4(), owner_id=faker.uuid4()
        )

        self.user = TestHelpers.create_test_user()

    def test_pre_analysis(self):
        with open("api/libs/fixtures/playlist-tracks.json") as f:
            data = json.load(f)

        cleaned_track_data = []

        for entry in Track.sync.before_sync(data.get("items")):
            cleaned_track_data.append(entry)

        track_results = Track.sync.sync(items=(data for data in cleaned_track_data))

        for track_pk, _ in track_results:
            self.playlist.tracks.add(track_pk)

        self.playlist.is_synced = True
        self.playlist.save()

        result = Analysis.sync.pre_analysis(self.playlist.pk, self.user.pk)

        self.assertEqual(len(result), len(data.get("items")))

    def test_analyze(self):
        with open("api/libs/fixtures/playlist-tracks.json") as f:
            data = json.load(f)

        cleaned_track_data = []

        for entry in Track.sync.before_sync(data.get("items")):
            cleaned_track_data.append(entry)

        track_results = Track.sync.sync(items=(data for data in cleaned_track_data))

        for track_pk, _ in track_results:
            self.playlist.tracks.add(track_pk)

        self.playlist.is_synced = True
        self.playlist.version = faker.uuid4()
        self.playlist.save()

        Analysis.sync.pre_analysis(self.playlist.pk, self.user.pk)

        data = [
            {
                "id": track_pk,
                "danceability": faker.random_number(digits=2),
                "energy": faker.random_number(digits=2),
                "key": faker.random_number(digits=1),
                "loudness": faker.random_number(digits=2),
                "mode": faker.random_number(digits=1),
                "speechiness": faker.random_number(digits=2),
                "acousticness": faker.random_number(digits=2),
                "instrumentalness": faker.random_number(digits=2),
                "liveness": faker.random_number(digits=2),
                "valence": faker.random_number(digits=2),
                "tempo": faker.random_number(digits=2),
                "duration_ms": faker.random_number(digits=5),
                "time_signature": faker.random_number(digits=1),
            }
            for track_pk, _ in track_results
        ]

        result = Analysis.sync.analyze(self.playlist.pk, self.user.pk, data)

        self.assertIsNotNone(result)
