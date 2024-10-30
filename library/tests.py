from unittest import mock

from django.test import TestCase


class PlaylistViewSetTestCase(TestCase):
    def setUp(self):
        pass

    @mock.patch("library.views.sync_playlists_from_request")
    def test_list_playlists(self, task: mock.MagicMock):
        pass

    @mock.patch("library.views.sync_playlist_from_request")
    def test_retrieve_playlist(self, task: mock.MagicMock):
        pass
