"""Spotify Request Params."""

import dataclasses


@dataclasses.dataclass
class RequestParams:
    """Request Params base class."""

    path_params: list[str] = []

    @property
    def q(self) -> str:
        """Build and return the query string."""
        return ""

    @property
    def as_dict(self) -> dict:
        """Return the dataclass as a dictionary."""
        return dataclasses.asdict(self)


@dataclasses.dataclass
class SpotifyTopTracksParams(RequestParams):
    """Spotify Top Tracks Request Params."""

    pass


@dataclasses.dataclass
class SpotifyTopArtistsParams(RequestParams):
    """Spotify Top Artists Request Params."""

    pass


@dataclasses.dataclass
class SpotifyFollowedArtistsParams(RequestParams):
    """Spotify Followed Artists Request Params."""

    pass
