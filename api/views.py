"""API Views."""

import dataclasses
import datetime
import enum
import logging
import os
import typing
from http import HTTPMethod

import httpx
import jwt
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseServerError,
    JsonResponse,
)
from django.shortcuts import redirect
from httpx import URL, Request
from rest_framework import views
from rest_framework.request import Request as DRFRequest

from api.models import AppUser
from server import settings

logger = logging.getLogger(__name__)


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

WEB_APP_URL = "http://localhost:5173"
REDIRECT_URI = "http://localhost:8000/api/login"


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


class MissingAPICredentialsError(HttpResponseServerError):
    """Missing API Credentials Response."""

    def __init__(self) -> None:
        """Missing API Credentials HTTP Response."""
        super().__init__("Missing Spotify API credentials.")


class RedirectURI:
    """Redirect URI wrapper."""

    _url: URL

    def __init__(self, url: URL) -> None:
        """Redirect URI Constructor."""
        self._uri = url

    @classmethod
    def from_request(cls: type["RedirectURI"], request: Request) -> str:
        """Create a RedirectURI from a Request."""
        return cls(url=request.url).as_str

    @property
    def as_str(self) -> str:
        """Return the URL as a string."""
        return str(self._uri)


class SpotifyAPITokenSet(typing.TypedDict):
    """Spotify API Token Set."""

    access_token: str
    refresh_token: str
    token_expiry: float


class SpotifyAPIStates(enum.StrEnum):
    """Possible values for state parameter in Spotify API."""

    LOGIN = "app-login"
    SIGNUP = "app-signup"


class SpotifyAPIEndpoints(enum.StrEnum):
    """Spotify API Endpoints."""

    Authorization = "https://accounts.spotify.com/authorize"
    Access_Token = "https://accounts.spotify.com/api/token"  # noqa: S105

    BASE_URL = "https://api.spotify.com/v1"
    Current_User = "me"


class SpotifyAPIScope(enum.StrEnum):
    """Available authentication scopes for Spotify API.

    See: https://developer.spotify.com/documentation/web-api/concepts/scopes/
    """

    # Images
    UGC_IMAGE_UPLOAD = "ugc-image-upload"

    # Spotify Connect
    USER_READ_PLAYBACK_STATE = "user-read-playback-state"
    USER_MODIFY_PLAYBACK_STATE = "user-modify-playback-state"
    USER_READ_CURRENTLY_PLAYING = "user-read-currently-playing"

    # Playback
    APP_REMOTE_CONTROL = "app-remote-control"
    STREAMING = "streaming"

    # Playlists
    PLAYLIST_READ_PRIVATE = "playlist-read-private"
    PLAYLIST_READ_COLLABORATIVE = "playlist-read-collaborative"
    PLAYLIST_MODIFY_PRIVATE = "playlist-modify-private"
    PLAYLIST_MODIFY_PUBLIC = "playlist-modify-public"

    # Follow
    USER_FOLLOW_MODIFY = "user-follow-modify"
    USER_FOLLOW_READ = "user-follow-read"

    # Listening History
    USER_READ_PLAYBACK_POSITION = "user-read-playback-position"
    USER_TOP_READ = "user-top-read"
    USER_READ_RECENTLY_PLAYED = "user-read-recently-played"

    # Library
    USER_LIBRARY_MODIFY = "user-library-modify"
    USER_LIBRARY_READ = "user-library-read"

    # Users
    USER_READ_EMAIL = "user-read-email"
    USER_READ_PRIVATE = "user-read-private"

    # Open Access
    USER_SOA_LINK = "user-soa-link"
    USER_SOA_UNLINK = "user-soa-unlink"
    SOA_MANAGE_ENTITLEMENTS = "soa-manage-entitlements"
    SOA_MANAGE_PARTNER = "soa-manage-partner"
    SOA_CREATE_PARTNER = "soa-create-partner"

    @classmethod
    def user_scopes(cls: type["SpotifyAPIScope"]) -> str:
        """Return a list of user scopes."""
        return " ".join(
            [
                cls.USER_READ_EMAIL,
                cls.USER_READ_PRIVATE,
                cls.USER_READ_PLAYBACK_STATE,
                cls.USER_MODIFY_PLAYBACK_STATE,
                cls.USER_READ_CURRENTLY_PLAYING,
                cls.USER_READ_PLAYBACK_POSITION,
                cls.USER_TOP_READ,
                cls.USER_READ_RECENTLY_PLAYED,
                cls.USER_LIBRARY_MODIFY,
                cls.USER_LIBRARY_READ,
                cls.USER_FOLLOW_MODIFY,
                cls.USER_FOLLOW_READ,
            ]
        )


class CallbackMixin(views.APIView):
    """Handle Callback Mixin."""

    def callback(self, request: DRFRequest) -> None:
        """OAuth2 Callback."""
        authorization_code = request.query_params.get("code")

        if not authorization_code:
            return

        pass


class AuthenticateMixin(views.APIView):
    """Handle Authentication Mixin."""

    def authenticate(self, request: DRFRequest) -> None:
        """Authenticate.

        Create a JWT and redirect to the frontend.

        i.e. /dashboard?token=JWT - The client is expected to
        store the JWT in localStorage and redirect to /dashboard.
        """
        pass


class SignupView(CallbackMixin):
    """Signup View."""

    pass


class LoginView(views.APIView):
    """Login View."""

    def get(self, request: DRFRequest) -> HttpResponse:
        """Spotify Callback.

        Endpoint: GET /api/login
        """
        logger.debug("Received a GET request to /api/login")

        authorization_code: str | None = request.query_params.get("code")
        state = request.query_params.get("state")

        if state != SpotifyAPIStates.LOGIN:
            return HttpResponseBadRequest()

        if not authorization_code or request.query_params.get("error") is not None:
            return HttpResponseForbidden()

        client_id = os.getenv("SPOTIFY_CLIENT_ID")
        client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

        if not client_id or not client_secret:
            return MissingAPICredentialsError()

        auth = httpx.BasicAuth(username=client_id, password=client_secret)

        # TODO: Create a type or dataclass for this object.
        data = {
            "grant_type": "authorization_code",
            "code": authorization_code,
            "redirect_uri": REDIRECT_URI,
        }

        token_set: SpotifyAPITokenSet = {
            "access_token": "",
            "refresh_token": "",
            "token_expiry": 0,
        }

        # TODO: Move to service layer.
        with httpx.Client(
            base_url=SpotifyAPIEndpoints.Access_Token, auth=auth
        ) as client:
            response = client.post(url="", data=data)

            if response.is_error:
                logger.error(f"Error: {response.text}")
                return HttpResponseBadRequest()

            resp = response.json()
            logger.debug(f"Response: {resp}")

            if not resp.get("access_token"):
                return HttpResponseBadRequest()

            client.close()

        current_unix_time = datetime.datetime.now().timestamp()

        token_set["access_token"] = resp.get("access_token")
        token_set["refresh_token"] = resp.get("refresh_token")
        token_set["token_expiry"] = current_unix_time + float(resp.get("expires_in", 0))

        logger.debug(f"Access token for expires at {token_set.get('token_expiry')}")

        # TODO: Move to service layer.
        with httpx.Client(
            base_url=SpotifyAPIEndpoints.BASE_URL,
            headers={"Authorization": f"Bearer {token_set.get("access_token")}"},
        ) as client:
            response = client.get(url=SpotifyAPIEndpoints.Current_User)

            if response.is_error:
                logger.error(f"Error: {response.text}")
                return HttpResponseBadRequest()

            resp = response.json()
            logger.debug(f"Response: {resp}")

            # TODO: Create a type or dataclass for this object.
            spotify_id = resp.get("id")
            spotify_email = resp.get("email")
            spotify_display_name = resp.get("display_name")

            if not spotify_id or not spotify_email:
                return HttpResponseBadRequest()

            timestamp = token_set.get("token_expiry")

            if not timestamp:
                return HttpResponseBadRequest()

            client.close()

        try:
            user = AppUser.objects.get(spotify_id=spotify_id)

            logger.debug(f"Found user: {user.public_id}")
        except AppUser.DoesNotExist:
            user = AppUser.objects.create(
                spotify_id=spotify_id,
                email=spotify_email,
                first_name=spotify_display_name,
                last_name="",
                access_token=token_set.get("access_token") or "",
                refresh_token=token_set.get("refresh_token") or "",
                token_expiry=datetime.datetime.fromtimestamp(timestamp),
            )

            user.save()

            user.refresh_from_db()

            logger.debug(f"Created user: {user.public_id}")

        client_jwt = Token(user)

        client = httpx.Client(base_url=WEB_APP_URL)

        req = client.build_request(
            HTTPMethod.GET,
            url="/dashboard",
            params={"token": client_jwt.encode()},  # NOTE can be used to look up user.
        )

        resp = redirect(to=RedirectURI.from_request(req))

        resp.headers["Access-Control-Allow-Origin"] = "*"

        logger.debug("Redirecting to dashboard.")

        return resp

    def post(self, request: DRFRequest) -> HttpResponse:
        """Login to Spotify.

        Endpoint: POST /api/login
        """
        client_id = os.getenv("SPOTIFY_CLIENT_ID")

        if not client_id:
            return MissingAPICredentialsError()

        # TODO: Create a type or dataclass for these params.
        params = {
            "client_id": client_id,
            "response_type": "code",
            "redirect_uri": REDIRECT_URI,
            "state": SpotifyAPIStates.LOGIN,
            "scope": SpotifyAPIScope.user_scopes(),
        }

        # TODO: Move to service layer.
        client = httpx.Client(base_url=SpotifyAPIEndpoints.Authorization)

        req = client.build_request(HTTPMethod.GET, url="", params=params)
        resp = redirect(to=RedirectURI.from_request(req))

        resp.headers["Access-Control-Allow-Origin"] = "*"

        logger.debug("Redirecting to Spotify for login.")
        logger.debug(f"Headers: {resp.headers}")

        return JsonResponse(data={"redirect": resp.url})


class ValidateView(views.APIView):
    """Validate View.

    Polled by the client to check if the JWT token is still valid.

    Endpoint: GET /api/validate
    """

    def post(self, request: DRFRequest) -> HttpResponse:
        """Validate the JWT token.

        Endpoint: GET /api/validate
        """
        token = request.headers.get("Authorization")

        if not token:
            return HttpResponseForbidden()

        tag, token = token.split(" ")

        if tag.lower() != "bearer":
            return HttpResponseForbidden()

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            logger.debug(f"Token expired for user {payload.get('public_id')}")
            return HttpResponseForbidden()
        except jwt.InvalidTokenError:
            logger.debug("Invalid token.")
            return HttpResponseForbidden()

        logger.debug(f"Found token for user {payload.get('public_id')}")

        try:
            user = AppUser.objects.get(public_id=payload.get("public_id"))

            logger.debug(f"Found user: {user.public_id} with pk {user.pk}")
        except AppUser.DoesNotExist:
            return HttpResponseForbidden(content={"message": "User not found."})

        return JsonResponse(data={"message": "Valid token."})
