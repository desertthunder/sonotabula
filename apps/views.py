"""Listening History views.

This module contains a single view that is
responsible for syncing recently played tracks
from the user's Spotify API listening history.

All three actions are essentially the same, they just
fetch a different amount of data. See the limit arg passed
to the service class.
"""

import typing

from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models.permissions import SpotifyAuth
from api.services.spotify import (
    AUTH,
    DATA,
    PLAYBACK,
    SpotifyAuthService,
    SpotifyDataService,
    SpotifyPlaybackService,
)
from apps.models import ListeningHistory, ListeningHistorySerializer
from apps.serializers import UserSavedItems
from core.views import GetUserMixin


class ListeningHistoryView(GetUserMixin, APIView):
    """Listening History view."""

    _data: SpotifyDataService
    _auth: SpotifyAuthService
    _playback: SpotifyPlaybackService

    authentication_classes = [SpotifyAuth]
    permission_classes = [IsAuthenticated]

    def __init__(
        self,
        data: SpotifyDataService = DATA,
        auth: SpotifyAuthService = AUTH,
        playback: SpotifyPlaybackService = PLAYBACK,
    ) -> None:
        """Initialize the view."""
        self._data = data
        self._auth = auth
        self._playback = playback

    def serialize(
        self, items: typing.Iterable[dict], user_pk: int
    ) -> list["ListeningHistorySerializer"]:
        """Serialize the data.

        Before saving the data to the database, we need to
        validate the data and build a ListeningHistory object.
        """
        for item in items:
            record = ListeningHistorySerializer.from_api(item)
            obj = ListeningHistory.history.build(record, user_pk)

        return [ListeningHistorySerializer.from_db(obj)]

    def get(self, request: Request) -> Response:
        """Get the user's listening history."""
        user = self.get_user(request)
        items = self._playback.recently_played(user.pk, 1)
        data = self.serialize(items, user.pk)

        return Response({"data": data[0].model_dump()})

    def put(self, request: Request) -> Response:
        """Refresh the user's listening history.

        It also syncs a small batch of data.
        """
        user = self.get_user(request)
        items = self._playback.recently_played(user.pk, 5)
        data = self.serialize(items, user.pk)

        return Response({"data": [item.model_dump() for item in data]})

    def post(self, request: Request) -> Response:
        """Sync the user's listening history.

        It also syncs a larger batch of data.
        """
        limit = request.query_params.get("limit", 50)
        user = self.get_user(request)
        items = self._playback.recently_played(user.pk, int(limit))
        data = self.serialize(items, user.pk)

        return Response({"data": [item.model_dump() for item in data]})


class UserSavedItemsView(GetUserMixin, APIView):
    """User saved items view."""

    _data: SpotifyDataService
    _auth: SpotifyAuthService
    _playback: SpotifyPlaybackService

    authentication_classes = [SpotifyAuth]
    permission_classes = [IsAuthenticated]

    def __init__(self, data: SpotifyDataService = DATA) -> None:
        """Initialize the view."""
        self._data = data

    def get(self, request: Request) -> Response:
        """Get user saved items."""
        user = self.get_user(request)
        data = self._data.fetch_saved_items(user, 1)
        items = UserSavedItems.get(data)
        return Response({"data": items.model_dump()})
