"""Listening History views."""

import typing

from loguru import logger
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models.permissions import SpotifyAuth
from api.services.spotify import (
    SpotifyAuthService,
    SpotifyDataService,
    SpotifyPlaybackService,
)
from apps.models import ListeningHistory, ListeningHistorySerializer
from core.models import AppUser

data_service = SpotifyDataService()
auth_service = SpotifyAuthService()
playback_service = SpotifyPlaybackService()


class ListeningHistoryView(APIView):
    """Listening History view."""

    data_service: SpotifyDataService
    auth_service: SpotifyAuthService
    playback_service: SpotifyPlaybackService

    authentication_classes = [
        SpotifyAuth,
    ]
    permission_classes = [
        IsAuthenticated,
    ]

    def __init__(
        self,
        data: SpotifyDataService = data_service,
        auth: SpotifyAuthService = auth_service,
        playback: SpotifyPlaybackService = playback_service,
    ) -> None:
        """Initialize the view."""
        self.data_service = data
        self.auth_service = auth
        self.playback_service = playback

    # (TODO) This will be replaced with a celery task
    def serialize(
        self, items: typing.Iterable[dict], user_pk: int
    ) -> list["ListeningHistorySerializer"]:
        """Serialize the data."""
        data = []
        for item in items:  # this will only iterate once
            record = ListeningHistorySerializer.from_api(item)
            obj = ListeningHistory.history.build(record, user_pk)
            logger.info(f"{obj.pk} - {obj.track.name}")

        data.append(ListeningHistorySerializer.from_db(obj))

        return data

    def get_user(self, request: Request) -> AppUser:
        """Get the user from the request."""
        return AppUser.objects.get(pk=request.user.pk)

    def get(self, request: Request) -> Response:
        """Get the user's listening history."""
        user = self.get_user(request)
        items = self.playback_service.recently_played(user.pk, 1)
        data = self.serialize(items, user.pk)

        return Response({"data": data[0].model_dump()})

    def put(self, request: Request) -> Response:
        """Refresh the user's listening history.

        It also syncs a small batch of data.
        """
        user = self.get_user(request)
        items = self.playback_service.recently_played(user.pk, 5)
        data = self.serialize(items, user.pk)

        return Response({"data": [item.model_dump() for item in data]})

    def post(self, request: Request) -> Response:
        """Sync the user's listening history.

        It also syncs a larger batch of data.
        """
        limit = request.query_params.get("limit", 50)
        user = self.get_user(request)
        items = self.playback_service.recently_played(user.pk, int(limit))
        data = self.serialize(items, user.pk)

        return Response({"data": [item.model_dump() for item in data]})
