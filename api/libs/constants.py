"""API Constants."""

import enum

WEB_APP_URL = "http://localhost:5173"
REDIRECT_URI = "http://localhost:8000/api/login"


class SpotifyAPIEndpoints(enum.StrEnum):
    """Spotify API Endpoints."""

    Authorization = "https://accounts.spotify.com/authorize"
    Access_Token = "https://accounts.spotify.com/api/token"  # noqa: S105

    BASE_URL = "https://api.spotify.com/v1"
    Current_User = "me"


class SpotifyAPIStates(enum.StrEnum):
    """Possible values for state parameter in Spotify API."""

    LOGIN = "app-login"
    SIGNUP = "app-signup"


class SpotifyAPIScopes(enum.StrEnum):
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
    def user_scopes(cls: type["SpotifyAPIScopes"]) -> str:
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
