"""Core API Views."""

from http import HTTPStatus

from pydantic import BaseModel
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from api.models.permissions import SpotifyAuth
from api.services.spotify.auth import SpotifyAuthService
from api.services.spotify.data import SpotifyDataService
from apps.views import UserSavedItems
from core.models import AppUser


class UserSerializer(BaseModel):
    """User Serializer."""

    spotify_id: str
    email: str
    display_name: str
    saved_tracks: int
    saved_albums: int
    saved_playlists: int
    saved_artists: int
    saved_shows: int
    id: str
    image_url: str | None = None

    @classmethod
    def from_api(
        cls: type["UserSerializer"], data: dict, user: AppUser
    ) -> "UserSerializer":
        """Create a UserSerializer from an API response."""
        return cls(
            id=str(user.public_id),
            spotify_id=data.get("id", user.spotify_id),
            email=user.email,
            display_name=data.get("display_name", user.spotify_display_name),
            image_url=data.get("images", [{}])[0].get("url", user.image_url),
            saved_tracks=user.saved_tracks,
            saved_albums=user.saved_albums,
            saved_playlists=user.saved_playlists,
            saved_artists=user.saved_artists,
            saved_shows=user.saved_shows,
        )

    @classmethod
    def from_db(cls: type["UserSerializer"], user: AppUser) -> "UserSerializer":
        """Create a UserSerializer from a database model."""
        return cls(
            id=str(user.public_id),
            spotify_id=user.spotify_id,
            email=user.email,
            display_name=user.spotify_display_name,
            image_url=user.image_url,
            saved_tracks=user.saved_tracks,
            saved_albums=user.saved_albums,
            saved_playlists=user.saved_playlists,
            saved_artists=user.saved_artists,
            saved_shows=user.saved_shows,
        )

    def update_counts(self, saved: UserSavedItems) -> "UserSerializer":
        """Update the saved item counts."""
        self.saved_tracks = saved.tracks
        self.saved_albums = saved.albums
        self.saved_playlists = saved.playlists
        self.saved_artists = saved.artists
        self.saved_shows = saved.shows

        return self

    def to_db(self, user: AppUser) -> AppUser:
        """Update a database model from a UserSerializer."""
        user.spotify_display_name = self.display_name
        user.image_url = self.image_url
        user.saved_tracks = self.saved_tracks
        user.saved_albums = self.saved_albums
        user.saved_playlists = self.saved_playlists
        user.saved_artists = self.saved_artists
        user.saved_shows = self.saved_shows

        user.save()
        return user


class ProfileViewSet(viewsets.ViewSet):
    """User profile view set."""

    authentication_classes = [SpotifyAuth]
    permission_classes = [IsAuthenticated]

    _auth: SpotifyAuthService = SpotifyAuthService()
    _data: SpotifyDataService = SpotifyDataService()

    def get_user(self, request: Request) -> AppUser:
        """Get the current user."""
        return AppUser.objects.get(id=request.user.id)

    def list(self, _: Request) -> Response:
        """Get the current user profile."""
        raise NotImplementedError

    def retrieve(self, request: Request) -> Response:
        """Get a user profile."""
        user = self.get_user(request)
        force = bool(request.query_params.get("force", False))

        if user.should_update or force:
            saved_res = self._data.fetch_saved_items(user)
            saved = UserSavedItems.get(saved_res)

            profile_res = self._auth.get_full_profile(user.pk)
            profile = UserSerializer.from_api(profile_res, user)
            profile = profile.update_counts(saved)

            profile.to_db(user)

            user.refresh_from_db()

        return Response(
            data={"data": UserSerializer.from_db(user).model_dump()},
            status=HTTPStatus.OK,
        )
