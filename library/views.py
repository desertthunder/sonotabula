"""Library Views & ViewSets."""

from http import HTTPStatus

from loguru import logger
from rest_framework import permissions, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from api.libs.constants import SpotifyAPIEndpoints
from api.models import Library, Playlist
from api.models.permissions import SpotifyAuth
from api.serializers.library import ExpandedPlaylist as ExpandedPlaylistSerializer
from api.serializers.library import Playlist as PlaylistSerializer
from api.serializers.library import Track as TrackSerializer
from api.serializers.library import TrackFeaturesSerializer
from api.services.spotify import (
    SpotifyAuthService,
    SpotifyDataService,
    SpotifyLibraryService,
)
from library.tasks import (
    sync_playlist_tracks_from_request,
    sync_playlists_from_request,
    sync_tracks_from_request,
)
from library.tasks.track import sync_track_features_from_request

AUTH = SpotifyAuthService()
LIBRARY = SpotifyLibraryService(auth_service=AUTH)
DATA = SpotifyDataService()


class ViewSetMixin:
    """ViewSet Mixin."""

    def get_page_params(self, request: Request) -> tuple[int, int, int]:
        """Get page size and page number from request query params."""
        page_size = request.query_params.get("page_size", 20)
        page = request.query_params.get("page", 1)
        offset = request.query_params.get("offset") or (int(page) - 1) * int(page_size)

        logger.info(f"Client query params: {page_size=}, {page=}, {offset=}")

        return int(page_size), int(page), int(offset)

    def get_user_library(self, user_id: int) -> Library:
        """Get a user's library."""
        library, created = Library.objects.get_or_create(user_id=user_id)

        if created:
            logger.debug(f"Created library for user {user_id}")

        return library


class PlaylistViewSet(viewsets.ViewSet):
    """Playlist ViewSet."""

    authentication_classes = [SpotifyAuth]
    permission_classes = [permissions.IsAuthenticated]

    _base_path = SpotifyAPIEndpoints.SavedPlaylists
    _auth: SpotifyAuthService = AUTH
    _library: SpotifyLibraryService = LIBRARY

    def get_model_instance(self, pk: str) -> Playlist:
        """Get a playlist instance by ID."""
        return Playlist.objects.get(id=pk)

    def get_user_library(self, user_id: int) -> Library:
        """Get a user's library."""
        library, created = Library.objects.get_or_create(user_id=user_id)

        if created:
            logger.debug(f"Created library for user {user_id}")

        return library

    def get_page_params(self, request: Request) -> tuple[int, int, int]:
        """Get page size and page number from request query params."""
        page_size = request.query_params.get("page_size", 20)
        page = request.query_params.get("page", 1)
        offset = request.query_params.get("offset") or (int(page) - 1) * int(page_size)

        logger.debug(f"Client query params: {page_size=}, {page=}, {offset=}")

        return int(page_size), int(page), int(offset)

    def list(self, request: Request, *args, **kwargs) -> Response:
        """List the current page of playlists.

        Fetched in real time from the Spotify API.
        """
        user_id = request.user.id
        page_size, page, offset = self.get_page_params(request)
        total = self._library.library_playlists_total(user_id)
        resp = self._library.library_playlists(user_id, limit=page_size, offset=offset)
        data = [PlaylistSerializer.get(playlist).model_dump() for playlist in resp]
        response = {"data": data, "page_size": page_size, "page": page, "total": total}
        return Response(data=response, status=HTTPStatus.OK)

    def create(self, request: Request, *args, **kwargs) -> Response:
        """Sync the current page of playlists."""
        user_id = request.user.id
        page_size, page, offset = self.get_page_params(request)
        resp = self._library.library_playlists(user_id, limit=page_size, offset=offset)
        data = [PlaylistSerializer.get(playlist).model_dump() for playlist in resp]
        response = {"message": "Syncing playlists..."}

        sync_playlists_from_request.s(user_id, data).apply_async()

        return Response(data=response, status=HTTPStatus.ACCEPTED)

    def retrieve(self, request: Request, spotify_id: str, *args, **kwargs) -> Response:
        """Retrieve a playlist by Spotify ID."""
        if spotify_id is None:
            logger.error(f"Spot: {spotify_id}")
            return Response(data={}, status=HTTPStatus.NOT_FOUND)

        user_id = request.user.id
        playlist = self._library.library_playlist(user_id, spotify_id)
        data = ExpandedPlaylistSerializer.get(playlist).model_dump()

        sync_playlist_tracks_from_request.s(user_id, data).apply_async()

        return Response(data=data, status=HTTPStatus.OK)

    def update(self, request: Request, pk: str) -> Response:
        """Complete sync of a playlist by ID."""
        raise NotImplementedError

    def partial_update(self, request: Request, pk: str) -> Response:
        """Sync playlist tracks by ID."""
        raise NotImplementedError

    def destroy(self, request: Request, pk: str) -> Response:
        """Unfollow a playlist."""
        raise NotImplementedError


class TrackViewSet(ViewSetMixin, viewsets.ViewSet):
    """Track ViewSet."""

    authentication_classes = [SpotifyAuth]
    permission_classes = [permissions.IsAuthenticated]

    _base_path = SpotifyAPIEndpoints.SavedTracks
    _auth: SpotifyAuthService = AUTH
    _library: SpotifyLibraryService = LIBRARY
    _data: SpotifyDataService = DATA

    def list(self, request: Request) -> Response:
        """List the current page of tracks."""
        user_id = request.user.id
        page_size, page, offset = self.get_page_params(request)
        total = self._library.library_tracks_total(user_id)
        resp = self._library.library_tracks(user_id, limit=page_size, offset=offset)
        data = [TrackSerializer.get(track).model_dump() for track in resp]
        response = {"data": data, "page_size": page_size, "page": page, "total": total}
        return Response(data=response, status=HTTPStatus.OK)

    def create(self, request: Request) -> Response:
        """Sync the current page of tracks."""
        user_id = request.user.id
        page_size, _, offset = self.get_page_params(request)
        resp = self._library.library_tracks(user_id, limit=page_size, offset=offset)
        data = [TrackSerializer.get(track).model_dump() for track in resp]
        response = {"message": "Syncing tracks..."}

        sync_tracks_from_request.s(user_id, data).apply_async()

        return Response(data=response, status=HTTPStatus.ACCEPTED)

    def retrieve(self, request: Request, spotify_id: str, *args, **kwargs) -> Response:
        """Retrieve a track by ID."""
        user_id = request.user.id
        track = self._library.library_track(user_id, spotify_id)
        data = TrackSerializer.get(track).model_dump()

        sync_tracks_from_request.s(user_id, [data]).apply_async()

        return Response(data=data, status=HTTPStatus.OK)

    def data(self, request: Request, spotify_id: str, *args, **kwargs) -> Response:
        """Retrieve a track by ID."""
        user_id = request.user.id
        features = self._data.fetch_audio_features_for_track(spotify_id, user_id)
        data = TrackFeaturesSerializer.get(features).model_dump()

        sync_track_features_from_request.s(user_id, spotify_id, data).apply_async()

        return Response(data=data, status=HTTPStatus.OK)

    def update(self, request: Request, pk: str) -> Response:
        """Update a track by ID."""
        raise NotImplementedError

    def partial_update(self, request: Request, pk: str) -> Response:
        """Partial update a track by ID."""
        raise NotImplementedError

    def destroy(self, request: Request, pk: str) -> Response:
        """Delete a track by ID."""
        raise NotImplementedError


class ArtistViewSet(viewsets.ViewSet):
    """Artist ViewSet."""

    def list(self, request: Request) -> Response:
        """List all artists."""
        raise NotImplementedError

    def create(self, request: Request) -> Response:
        """Create a new artist."""
        raise NotImplementedError

    def retrieve(self, request: Request, pk: str) -> Response:
        """Retrieve an artist by ID."""
        raise NotImplementedError

    def update(self, request: Request, pk: str) -> Response:
        """Update an artist by ID."""
        raise NotImplementedError

    def partial_update(self, request: Request, pk: str) -> Response:
        """Partial update an artist by ID."""
        raise NotImplementedError

    def destroy(self, request: Request, pk: str) -> Response:
        """Delete an artist by ID."""
        raise NotImplementedError


class AlbumViewSet(viewsets.ViewSet):
    """Album ViewSet."""

    def list(self, request: Request) -> Response:
        """List all albums."""
        raise NotImplementedError

    def create(self, request: Request) -> Response:
        """Create a new album."""
        raise NotImplementedError

    def retrieve(self, request: Request, pk: str) -> Response:
        """Retrieve an album by ID."""
        raise NotImplementedError

    def update(self, request: Request, pk: str) -> Response:
        """Update an album by ID."""
        raise NotImplementedError

    def partial_update(self, request: Request, pk: str) -> Response:
        """Partial update an album by ID."""
        raise NotImplementedError

    def destroy(self, request: Request, pk: str) -> Response:
        """Delete an album by ID."""
        raise NotImplementedError
