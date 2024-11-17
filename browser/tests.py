import random
import unittest
from unittest import mock

from django.db import models
from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse
from faker import Faker
from rest_framework.request import Request

from api.libs.helpers import TestHelpers
from api.models import Album, Artist, Playlist, Track, TrackFeatures
from api.models.analysis import Analysis
from browser.filters import AlbumFilterSet, PlaylistFilterSet, TrackFilterSet
from browser.models import Library
from core.models import AppUser
from core.permissions import TokenSerializer

fake = Faker()


class FakeTaskResult:
    task_id: str
    status: str

    def __init__(self, task_id: str, task_status: str = "PENDING") -> None:
        self.task_id = task_id
        self.status = task_status

    @classmethod
    def new(
        cls: type["FakeTaskResult"],
        task_id: str = "fake-test-id",
    ) -> "FakeTaskResult":
        return cls(task_id)


def create_library_with_albume(user: AppUser, count: int = 10):
    library, _ = Library.objects.get_or_create(user=user)

    for i in range(count):
        artists = [
            Artist.objects.create(name=fake.name(), spotify_id=str(fake.uuid4()))
            for _ in range(fake.random_int(1, 5))
        ]

        album = Album.objects.create(
            name=fake.name(),
            spotify_id=str(fake.uuid4()),
            release_year=fake.year(),
        )

        album.artists.add(*artists)

        for _ in range(fake.random_int(7, 10)):
            album.tracks.add(
                Track.objects.create(
                    name=fake.name(),
                    spotify_id=str(fake.uuid4()),
                    duration=fake.random_int(1000, 10000),
                )
            )

        library.albums.add(album)

        create_analysis_from_album(album, library, force=(i < 2))

    return library


def create_library_with_playlists(user: AppUser, count: int = 10):
    library, _ = Library.objects.get_or_create(user=user)

    for i in range(count):
        playlist = Playlist.objects.create(
            name=fake.name(),
            spotify_id=str(fake.uuid4()),
            owner_id=user.spotify_id,
            version=str(fake.uuid4()),
        )

        playlist.tracks.add(
            *[create_track_with_features() for _ in range(fake.random_int(7, 10))]
        )

        library.playlists.add(playlist)

        create_analysis_from_playlist(playlist, library, force=(i < 2))

        playlist.is_analyzed = True
        playlist.is_synced = True

        playlist.save()
        library.save()

    return library


def create_analysis_from_playlist(
    playlist: Playlist, library: Library, force: bool = False
) -> Analysis | None:
    if not force and fake.boolean():
        return None

    analysis = Analysis.objects.create(
        playlist=playlist,
        version=str(playlist.version),
        user=library.user,
    )

    analysis.tracks.add(*playlist.tracks.all())

    return analysis


def create_analysis_from_album(
    album: Album, library: Library, force: bool = False
) -> Analysis | None:
    if not force and fake.boolean():
        return None

    analysis = Analysis.objects.create(
        album=album,
        version=str(album.updated_at.timestamp()),
        user=library.user,
    )

    analysis.tracks.add(*album.tracks.all())

    album.is_analyzed = True
    album.is_synced = True

    album.save()

    return analysis


def create_track_with_features():
    track = Track.objects.create(
        name=fake.name(),
        spotify_id=str(fake.uuid4()),
        duration=fake.random_int(1000, 10000),
    )

    TrackFeatures.objects.create(
        track=track,
        danceability=fake.random_number(digits=2) / 100,
        energy=fake.random_number(digits=2) / 100,
        key=fake.random_number(digits=2),
        loudness=fake.random_number(digits=2),
        mode=fake.random_number(digits=2),
        speechiness=fake.random_number(digits=2) / 100,
        acousticness=fake.random_number(digits=2) / 100,
        instrumentalness=fake.random_number(digits=2) / 100,
        liveness=fake.random_number(digits=2) / 100,
        valence=fake.random_number(digits=2) / 100,
        tempo=fake.random_number(digits=3),
        duration_ms=fake.random_number(digits=5),
        time_signature=fake.random_number(digits=2),
    )

    track.save()

    return track


class AlbumViewSetTestCase(TestCase):
    def setUp(self):
        self.user = TestHelpers.create_test_user()
        self.library = create_library_with_albume(self.user)
        self.jwt = TokenSerializer.from_user(user=self.user).encode()

    def test_list_albums_view(self):
        path = reverse("browser__albums")
        response = self.client.get(
            path,
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data["data"]), 10)
        self.assertEqual(data["pagination"]["total"], 10)

    def test_retrieve_album_view(self):
        album = fake.random_element(self.library.albums.all())
        artists = album.artists.all()
        tracks = album.tracks.all()
        response = self.client.get(
            reverse("browser__album", kwargs={"album_pk": str(album.id)}),
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["data"]["id"], str(album.id))
        self.assertEqual(data["data"]["name"], album.name)
        self.assertEqual(data["data"]["release_year"], album.release_year)
        self.assertEqual(len(data["data"]["artists"]), artists.count())
        self.assertEqual(len(data["data"]["tracks"]), tracks.count())


class AlbumMetadataViewSetTestCase(TestCase):
    def setUp(self):
        self.user = TestHelpers.create_test_user()
        self.library = create_library_with_albume(self.user)
        self.jwt = TokenSerializer.from_user(user=self.user).encode()

    def test_get_metadata(self):
        response = self.client.get(
            reverse("browser__albums-meta"),
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            data.get("total_synced"), Album.objects.filter(is_synced=True).count()
        )
        self.assertEqual(
            data.get("total_analyzed"), Album.objects.filter(is_analyzed=True).count()
        )
        self.assertEqual(
            data.get("total_tracks"),
            Album.objects.filter(is_synced=True)
            .aggregate(track_count=models.Count("tracks"))
            .get("track_count"),
        )


class PlaylistViewSetTestCase(TestCase):
    def setUp(self):
        self.user = TestHelpers.create_test_user()
        self.library = create_library_with_playlists(self.user)
        self.jwt = TokenSerializer.from_user(user=self.user).encode()

    def test_list_playlists_view(self):
        response = self.client.get(
            reverse("browser__playlists"),
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data["data"]), 10)
        self.assertEqual(data["pagination"]["total"], 10)

    @mock.patch("browser.tasks.sync_playlist.s")
    @mock.patch("celery.group.apply_async")
    def test_create_playlists_view(
        self, mock_group: mock.MagicMock, mock_sync_playlist: mock.MagicMock
    ):
        mock_group.return_value = FakeTaskResult("fake-task-id")
        page_size = fake.random_int(1, 10)
        path = reverse("browser__playlists")
        response = self.client.post(
            f"{path}?page_size={page_size}",
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        data = response.json()

        self.assertEqual(mock_sync_playlist.call_count, page_size)
        self.assertEqual(mock_group.call_count, 1)
        self.assertEqual(response.status_code, 202)
        self.assertEqual(data["status"], "PENDING")

    @mock.patch("browser.tasks.analyze_playlist.apply_async")
    @mock.patch("browser.tasks.sync_playlist.apply_async")
    def test_partial_update_playlists_view(
        self,
        mock_sync_playlist: mock.MagicMock,
        mock_analyze_playlist: mock.MagicMock,
    ):
        mock_sync_playlist.return_value = FakeTaskResult.new()
        mock_analyze_playlist.return_value = FakeTaskResult.new()
        playlist: Playlist = fake.random_element(self.library.playlists.all())
        response = self.client.patch(
            reverse("browser__playlist", kwargs={"playlist_pk": str(playlist.id)}),
            content_type="application/json",
            headers={"Authorization": f"Bearer {self.jwt}"},
            data={"operation": "analyze"},
        )
        data = response.json()

        self.assertEqual(mock_sync_playlist.call_count, 0)
        self.assertEqual(mock_analyze_playlist.call_count, 1)
        self.assertEqual(response.status_code, 202)
        self.assertEqual(data["status"], "PENDING")

    @mock.patch("browser.tasks.sync_and_analyze_playlist.apply_async")
    def test_update_playlists_view(
        self, mock_sync_and_analyze_playlist: mock.MagicMock
    ):
        mock_sync_and_analyze_playlist.return_value = FakeTaskResult.new()
        playlist: Playlist = fake.random_element(self.library.playlists.all())
        response = self.client.put(
            reverse("browser__playlist", kwargs={"playlist_pk": str(playlist.id)}),
            headers={"Authorization": f"Bearer {self.jwt}"},
            content_type="application/json",
        )
        data = response.json()

        self.assertEqual(mock_sync_and_analyze_playlist.call_count, 1)
        self.assertEqual(response.status_code, 202)
        self.assertEqual(data["status"], "PENDING")

    def test_destroy_playlist_view(self):
        response = self.client.delete(
            reverse(
                "browser__playlist",
                kwargs={
                    "playlist_pk": str(self.library.playlists.first().id),
                },
            ),
            headers={"Authorization": f"Bearer {self.jwt}"},
        )

        self.assertEqual(response.status_code, 405)


class PlaylistMetadataViewSetTestCase(TestCase):
    def setUp(self):
        self.user = TestHelpers.create_test_user()
        self.library = create_library_with_playlists(self.user)
        self.jwt = TokenSerializer.from_user(user=self.user).encode()

    def test_get_metadata(self):
        response = self.client.get(
            reverse("browser__playlists-meta"),
            headers={"Authorization": f"Bearer {self.jwt}"},
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            data.get("total_synced"), Playlist.objects.filter(is_synced=True).count()
        )
        self.assertEqual(
            data.get("total_analyzed"),
            Playlist.objects.filter(is_analyzed=True).count(),
        )
        self.assertEqual(
            data.get("total_tracks"),
            Playlist.objects.filter(is_synced=True)
            .aggregate(track_count=models.Count("tracks"))
            .get("track_count"),
        )


class PlaylistFilterSetTestCase(TestCase):
    """Test PlaylistFilterSet."""

    def setUp(self) -> None:
        """Set up test data."""
        self.user = TestHelpers.create_test_user()
        self.filters = PlaylistFilterSet()
        self.request = Request(HttpRequest())
        self.library, _ = Library.objects.get_or_create(user=self.user)

        for _ in range(10):
            playlist = Playlist.objects.create(
                name=fake.name() + "__FILTER__",
                spotify_id=str(fake.uuid4()),
                owner_id=self.user.spotify_id,
                public=True,
                shared=True,
                is_analyzed=random.choice([True, False]),
                is_synced=random.choice([True, False]),
            )

            for _ in range(10):
                album = Album.objects.create(
                    name=fake.name() + "__ALBUM__",
                    spotify_id=str(fake.uuid4()),
                    release_year=fake.year(),
                    image_url=fake.image_url(),
                    album_type=fake.word(),
                )

                playlist.tracks.add(
                    Track.objects.create(
                        album=album,
                        name=fake.name() + "__TRACK__",
                        spotify_id=str(fake.uuid4()),
                        duration=fake.random_number(digits=3),
                    )
                )

            playlist.save()

            self.library.playlists.add(playlist)

        self.playlist = random.choice(Playlist.objects.all())

        self.request.user = self.user

    def test_get_queryset(self):
        """Test get_queryset."""
        queryset = self.filters.get_queryset(self.request)
        self.assertIsNotNone(queryset)
        self.assertEqual(
            queryset.count(),
            Playlist.objects.filter(libraries__user=self.user).count(),
        )

    def test_filter_name(self):
        """Test filter_name."""
        name = "__FILTER__"
        queryset = Playlist.objects.all()
        filtered_queryset = self.filters.filter_name(queryset, name)
        self.assertEqual(filtered_queryset.count(), 10)

    def test_filter_public(self):
        """Test filter_public."""
        queryset = Playlist.objects.all()
        filtered_queryset = self.filters.filter_public(queryset, True)
        self.assertGreater(filtered_queryset.count(), 0)

    def test_filter_collaborative(self):
        """Test filter_collaborative."""
        queryset = Playlist.objects.all()
        filtered_queryset = self.filters.filter_collaborative(queryset, True)
        self.assertGreater(filtered_queryset.count(), 0)

    def test_filter_my_playlists(self):
        """Test filter_my_playlist."""
        queryset = Playlist.objects.all()
        filtered_queryset = self.filters.filter_my_playlists(
            queryset, self.user.spotify_id, self.request
        )
        self.assertEqual(filtered_queryset.count(), 10)

    def test_filter_is_analyzed(self):
        """Test filter_is_analyzed."""
        queryset = Playlist.objects.all()
        filtered_queryset = self.filters.filter_is_analyzed(queryset, 1)
        self.assertGreater(filtered_queryset.count(), 0)

    def test_filter_is_synced(self):
        """Test filter_is_synced."""
        queryset = Playlist.objects.all()
        filtered_queryset = self.filters.filter_is_synced(queryset, 1)
        self.assertGreater(filtered_queryset.count(), 0)

    def test_filter_private(self):
        """Test filter_private."""
        queryset = Playlist.objects.all()
        filtered_queryset = self.filters.filter_private(queryset, 1)
        self.assertGreater(filtered_queryset.count(), 0)

    def test_filter_num_tracks(self):
        """Test filter_num_tracks."""
        queryset = Playlist.objects.all()
        filtered_queryset = self.filters.filter_num_tracks(queryset, 5)
        self.assertGreater(filtered_queryset.count(), 0)

    def test_filter_track_name(self):
        """Test filter_track_name."""
        queryset = Playlist.objects.all()
        filtered_queryset = self.filters.filter_track_name(queryset, "__TRACK__")
        self.assertEqual(filtered_queryset.count(), 100)


@unittest.skip("TODO")
class TrackFilterSetTestCase(TestCase):
    def setUp(self) -> None:
        self.user = TestHelpers.create_test_user()
        self.analysis = Analysis.objects.prefetch_related("playlist").first()

        if not self.analysis:
            self.fail("No analysis found.")

        self.playlist = self.analysis.playlist
        self.filters = TrackFilterSet()
        self.request = Request(HttpRequest())
        self.fake_album = Album.objects.create(
            name=fake.name() + "__ALBUM__",
            spotify_id=str(fake.uuid4()),
            release_year=fake.year(),
            image_url=fake.image_url(),
            album_type=fake.word(),
        )

        self.fake_track = Track.objects.create(
            name=fake.name() + "__TRACK__",
            spotify_id=str(fake.uuid4()),
            duration=fake.random_number(digits=3),
            album=self.fake_album,
        )

    def test_call_method(self):
        """Test __call__ method."""
        queryset = self.filters(self.request)
        all_tracks = queryset.count()
        self.assertIsNotNone(queryset)
        self.assertGreater(all_tracks, 0)

        queryset_from_pl = self.filters(self.request, playlist_pk=self.playlist.pk)
        pl_tracks = queryset_from_pl.count()
        self.assertIsNotNone(queryset_from_pl)
        self.assertGreater(pl_tracks, 0)
        self.assertGreater(all_tracks, pl_tracks)

        queryset_with_features = self.filters(self.request, include_features=True)
        self.assertIsNotNone(queryset_with_features)
        self.assertGreater(queryset_with_features.count(), 0)
        self.assertIsNotNone(
            queryset_with_features.filter(id__in=self.analysis.tracks.all())
        )

    def test_filter_name(self):
        """Test filter_name."""
        name = "__TRACK__"
        queryset = self.filters.Meta.default_queryset
        filtered_queryset = self.filters.filter_name(queryset, name)
        self.assertEqual(filtered_queryset.count(), 1)

    def test_filter_album(self):
        """Test filter_album."""
        name = "__ALBUM__"
        queryset = self.filters.Meta.default_queryset
        filtered_queryset = self.filters.filter_album(queryset, name)
        self.assertEqual(filtered_queryset.count(), 1)


@unittest.skip("TODO")
class AlbumFilterSetTestCase(TestCase):
    """Test AlbumFilterSet."""

    def setUp(self) -> None:
        """Set up test data."""
        self.user = TestHelpers.create_test_user()
        self.filters = AlbumFilterSet()
        self.request = Request(HttpRequest())
        self.library = Library.objects.get(user=self.user)
        self.year = int(fake.year())

        self.years = (
            [self.year + 10 for _ in range(5)]
            + [self.year for _ in range(5)]
            + [self.year - 10 for _ in range(5)]
        )

        for year in self.years:
            Album.objects.create(
                name=fake.name() + "__FILTER__",
                spotify_id=str(fake.uuid4()),
                release_year=year,
                image_url=fake.image_url(),
                album_type=fake.word(),
            )

        self.album = random.choice(Album.objects.all())
        self.request.user = self.user

    def test_get_queryset(self):
        """Test get_queryset."""
        queryset = self.filters.get_queryset(self.request)
        self.assertIsNotNone(queryset)
        self.assertEqual(
            queryset.count(),
            Album.objects.filter(libraries__user=self.user).count(),
        )

    def test_filter_name(self):
        """Test filter_name."""
        name = "__FILTER__"
        queryset = Album.objects.all()
        filtered_queryset = self.filters.search_name(queryset, name)
        self.assertEqual(filtered_queryset.count(), 15)

    def test_filter_release_year(self):
        """Test filter_release_year."""
        name = "__FILTER__"
        queryset = self.filters.search_name(Album.objects.all(), name)
        filtered_queryset = self.filters.filter_release_year(queryset, self.year)
        self.assertEqual(filtered_queryset.count(), 5)

    def test_filter_released_before(self):
        """Test filter_released_before."""
        name = "__FILTER__"
        queryset = self.filters.search_name(Album.objects.all(), name)
        filtered_queryset = self.filters.filter_released_before(queryset, self.year)
        self.assertEqual(filtered_queryset.count(), 5)

    def test_filter_released_after(self):
        """Test filter_released_after."""
        name = "__FILTER__"
        queryset = self.filters.search_name(Album.objects.all(), name)
        filtered_queryset = self.filters.filter_released_after(queryset, self.year)
        self.assertEqual(filtered_queryset.count(), 5)
