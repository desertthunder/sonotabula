"""Custom Permission classes.

NOTE - when other services are added, the Token base class
and payload will have to be refactored.
"""

import dataclasses

import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request

from api.models import AppUser
from server import settings


class SpotifyAuth(BaseAuthentication):
    """Spotify Authentication."""

    def authenticate(self, request: Request) -> tuple[AppUser, str]:
        """Authenticate the request and return a two-tuple of (user, token)."""
        if "Authorization" in request.headers:
            user_email = self.authenticate_header(request)
            user = AppUser.objects.get(email=user_email)

            return user, user.access_token

        raise AuthenticationFailed("Authentication credentials were not provided.")

    def authenticate_header(self, request: Request) -> str | None:
        """Decodes the JWT token and returns the payload."""
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
            user_email = Token.decode_jwt(token)

            return user_email
        raise AuthenticationFailed("Authentication credentials were not provided.")


@dataclasses.dataclass
class TokenPayload:
    """Payload to generate a JWT token."""

    spotify_id: str | None
    public_id: str | None
    spotify_access_token: str
    email: str

    @property
    def as_dict(self) -> dict:
        """Return the payload as a dictionary."""
        return dataclasses.asdict(self)


class Token:
    """JWT Token."""

    secret: str = settings.SECRET_KEY
    algorithm: str = "HS256"
    token: str
    payload: TokenPayload

    def __init__(self, user: AppUser) -> None:
        """Token Constructor."""
        self.payload = TokenPayload(
            spotify_id=user.spotify_id,
            public_id=str(user.public_id) if user.public_id else None,
            email=user.email,
            spotify_access_token=user.access_token,
        )

    def encode(self) -> str:
        """Encode the JWT token."""
        return jwt.encode(self.payload.as_dict, self.secret, algorithm=self.algorithm)

    def decode(self, token: str) -> TokenPayload:
        """Decode the JWT token."""
        payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])

        return TokenPayload(
            spotify_id=payload.get("spotify_id"),
            public_id=payload.get("public_id"),
            email=payload.get("email"),
            spotify_access_token=payload.get("spotify_access_token"),
        )

    @classmethod  # TODO: This needs to change
    def decode_jwt(cls: type["Token"], jwt_token: str) -> str:
        """Create a Token from a token string."""
        payload = jwt.decode(jwt_token, cls.secret, algorithms=[cls.algorithm])
        return payload.get("email")
