"""Pydantic models for authentication."""

import typing

import jwt
from httpx import URL, Request
from pydantic import BaseModel

from core.models import AppUser
from server import settings


class RedirectURI(BaseModel):
    """Redirect URI wrapper."""

    url: str

    @classmethod
    def from_request(cls: type["RedirectURI"], request: Request) -> "RedirectURI":
        """Create a RedirectURI from a Request."""
        if not isinstance(request.url, URL):
            raise ValueError("Invalid URL object.")
        return cls(url=str(request.url))


class JWTPayloadSerializer(BaseModel):
    """Payload to generate a JWT token."""

    email: str
    spotify_access_token: str
    spotify_id: str | None
    public_id: str | None


class TokenSerializer(BaseModel):
    """JWT Token."""

    algorithm: typing.Literal["HS256"] = "HS256"
    secret: str = settings.SECRET_KEY
    token: str
    payload: JWTPayloadSerializer

    @classmethod
    def from_user(cls: type["TokenSerializer"], user: AppUser) -> "TokenSerializer":
        """Create a Token from a user."""
        t = cls.model_construct()
        t.payload = JWTPayloadSerializer(
            spotify_id=user.spotify_id,
            public_id=str(user.public_id) if user.public_id else None,
            email=user.email,
            spotify_access_token=user.access_token,
        )

        t.token = t.encode()

        return cls(**t.model_dump())

    @classmethod
    def get_payload(
        cls: type["TokenSerializer"],
        jwt_token: str,
    ) -> JWTPayloadSerializer:
        """Create a Token from a token string."""
        data = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=["HS256"])
        return JWTPayloadSerializer(**data)

    def encode(self) -> str:
        """Encode the JWT token."""
        return jwt.encode(
            self.payload.model_dump(),
            self.secret,
            algorithm=self.algorithm,
        )

    def decode(self, token: str) -> JWTPayloadSerializer:
        """Decode the JWT token."""
        payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])

        return JWTPayloadSerializer(
            spotify_id=payload.get("spotify_id"),
            public_id=payload.get("public_id"),
            email=payload.get("email"),
            spotify_access_token=payload.get("spotify_access_token"),
        )


class UserSavedItemSerializer(BaseModel):
    """User saved item totals."""

    artists: int
    albums: int
    tracks: int
    playlists: int
    shows: int

    @classmethod
    def get(
        cls: type["UserSavedItemSerializer"],
        iter: typing.Iterable[tuple[str, dict]],
    ) -> "UserSavedItemSerializer":
        """Get user saved items."""
        response = {
            "artists": 0,
            "albums": 0,
            "tracks": 0,
            "playlists": 0,
            "shows": 0,
        }

        for item, data in iter:
            key = item.split("/")[-1]

            if key == "following":
                response["artists"] = data["total"]
            else:
                response[key] = data["total"]

        return cls(**response)


class UserProfileSerializer(BaseModel):
    """A serialized user profile using AppUser records & saved items."""

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
        cls: type["UserProfileSerializer"], data: dict, user: AppUser
    ) -> "UserProfileSerializer":
        """Create a UserProfileSerializer from an API response."""
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
    def from_db(
        cls: type["UserProfileSerializer"], user: AppUser
    ) -> "UserProfileSerializer":
        """Create a UserProfileSerializer from a database model."""
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

    def update_counts(self, saved: UserSavedItemSerializer) -> "UserProfileSerializer":
        """Update the saved item counts."""
        self.saved_tracks = saved.tracks
        self.saved_albums = saved.albums
        self.saved_playlists = saved.playlists
        self.saved_artists = saved.artists
        self.saved_shows = saved.shows

        return self

    def to_db(self, user: AppUser) -> AppUser:
        """Update a database model from a UserProfileSerializer."""
        user.spotify_display_name = self.display_name
        user.saved_tracks = self.saved_tracks
        user.saved_albums = self.saved_albums
        user.saved_playlists = self.saved_playlists
        user.saved_artists = self.saved_artists
        user.saved_shows = self.saved_shows
        if image_url := self.image_url:
            user.image_url = image_url

        user.save()

        return user
