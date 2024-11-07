from unittest import mock

from django.test import TestCase
from django.urls import reverse
from faker import Faker

from api.libs.helpers import SpotifyAuthServiceMock
from api.models import Album, Artist, Playlist, Track
from api.models.permissions import Token
from browser.models import Library
from core.models import AppUser

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
    library = Library.objects.create(user=user)

    for _ in range(count):
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

    return library


def create_library_with_playlists(user: AppUser, count: int = 10):
    library = Library.objects.create(user=user)

    for _ in range(count):
        playlist = Playlist.objects.create(
            name=fake.name(),
            spotify_id=str(fake.uuid4()),
            owner_id=user.spotify_id,
        )
        playlist.tracks.add(
            *[
                Track.objects.create(
                    name=fake.name(),
                    spotify_id=str(fake.uuid4()),
                    duration=fake.random_int(1000, 10000),
                )
                for _ in range(fake.random_int(1, 5))
            ]
        )
        library.playlists.add(playlist)

    return library


class AlbumViewSetTestCase(TestCase):
    def setUp(self):
        self.user = AppUser.objects.from_spotify(
            SpotifyAuthServiceMock.get_current_user(),
            SpotifyAuthServiceMock.get_access_token(),
        )
        self.library = create_library_with_albume(self.user)
        self.jwt = Token(user=self.user).encode()

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


class PlaylistViewSetTestCase(TestCase):
    def setUp(self):
        self.user = AppUser.objects.from_spotify(
            SpotifyAuthServiceMock.get_current_user(),
            SpotifyAuthServiceMock.get_access_token(),
        )
        self.library = create_library_with_playlists(self.user)
        self.jwt = Token(user=self.user).encode()

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
