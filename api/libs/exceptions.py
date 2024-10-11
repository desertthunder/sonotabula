"""Custom API Exceptions.

TODO - Evaluate need for additional, domain specific exceptions.

TODO - Add more specific exceptions for the Spotify API.
TODO - Move the spotify exceptions to the spotify service module.
"""

from django.http import HttpResponseServerError


class MissingAPICredentialsResponse(HttpResponseServerError):  # noqa: N818
    """Missing API Credentials Response.

    This exception is raised when the Spotify API credentials are
    likely due to the environment variables not being set.
    """

    def __init__(self) -> None:
        """Missing API Credentials HTTP Response."""
        super().__init__(content="Missing Spotify API credentials.")


class MissingAPICredentialsError(Exception):
    """Missing API Credentials Error.

    This exception is raised when the Spotify API credentials are missing.
    """

    def __init__(self) -> None:
        """Missing API Credentials Error."""
        super().__init__("Missing Spotify API credentials.")


class SpotifyAPIError(Exception):
    """Spotify API Error.

    This exception is raised when an error occurs with the Spotify API.
    """

    def __init__(self, message: str) -> None:
        """Spotify API Error."""
        super().__init__(message)


class SpotifyExpiredTokenError(SpotifyAPIError):
    """Expired Token Error."""

    pass
