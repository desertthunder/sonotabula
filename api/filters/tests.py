from django.http import HttpRequest
from django.test import TestCase
from faker import Faker
from rest_framework.request import Request

from api.filters.playlist import PlaylistFilterSet
from api.models import AppUser
from api.models.music import Library
from api.models.playlist import Playlist

faker = Faker()


class PlaylistFilterSetTestCase(TestCase):
    """Test PlaylistFilterSet."""

    def setUp(self) -> None:
        """Set up test data."""
        self.user = AppUser.objects.get(is_staff=True)
        self.filters = PlaylistFilterSet()
        self.request = Request(HttpRequest())
        self.library = Library.objects.get(user=self.user)

        for _ in range(10):
            Playlist.objects.create(
                name=faker.name() + "__FILTER__",
                spotify_id=str(faker.uuid4()),
                owner_id=self.user.spotify_id,
                public=True,
                shared=True,
            )

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

    def test_filter_my_playlist(self):
        """Test filter_my_playlist."""
        queryset = Playlist.objects.all()
        filtered_queryset = self.filters.filter_my_playlist(
            queryset, self.user.spotify_id
        )
        self.assertGreater(filtered_queryset.count(), 10)

    def test_filter_is_analyzed(self):
        """Test filter_is_analyzed."""
        queryset = Playlist.objects.all()
        filtered_queryset = self.filters.filter_is_analyzed(queryset)
        self.assertGreater(filtered_queryset.count(), 0)

    def test_filter_is_synced(self):
        """Test filter_is_synced."""
        queryset = Playlist.objects.all()
        filtered_queryset = self.filters.filter_is_synced(queryset)
        self.assertGreater(filtered_queryset.count(), 0)

    def test_filter_private(self):
        """Test filter_private."""
        queryset = Playlist.objects.all()
        filtered_queryset = self.filters.filter_private(queryset)
        self.assertGreater(filtered_queryset.count(), 0)

    def test_filter_num_tracks(self):
        """Test filter_num_tracks."""
        queryset = Playlist.objects.all()
        filtered_queryset = self.filters.filter_num_tracks(queryset, 5)
        self.assertGreater(filtered_queryset.count(), 0)
