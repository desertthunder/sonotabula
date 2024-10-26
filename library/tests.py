from unittest import mock

from django.test import TestCase


# Create your tests here.
class PlaylistViewSetTestCase(TestCase):
    def setUp(self):
        pass

    @mock.patch("library.views.sync_playlists_from_request")
    def test_list_playlists(self, task: mock.MagicMock):
        pass
