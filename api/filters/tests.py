from django.http import HttpRequest
from django.test import TestCase
from faker import Faker
from rest_framework.request import Request

from api.filters.playlist import PlaylistFilterSet
from api.filters.tracks import TrackFilterSet
from api.models import Analysis, AppUser, Library, Playlist
from api.models.music import Album
from api.models.track import Track

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


class TrackFilterSetTestCase(TestCase):
    def setUp(self) -> None:
        self.user = AppUser.objects.get(is_staff=True)

        self.analysis = Analysis.objects.prefetch_related("playlist").first()

        if not self.analysis:
            self.fail("No analysis found.")

        self.playlist = self.analysis.playlist
        self.filters = TrackFilterSet()
        self.request = Request(HttpRequest())
        self.fake_album = Album.objects.create(
            name=faker.name() + "__ALBUM__",
            spotify_id=str(faker.uuid4()),
            release_year=faker.year(),
            image_url=faker.image_url(),
            album_type=faker.word(),
        )

        self.fake_track = Track.objects.create(
            name=faker.name() + "__TRACK__",
            spotify_id=str(faker.uuid4()),
            duration=faker.random_number(digits=3),
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
