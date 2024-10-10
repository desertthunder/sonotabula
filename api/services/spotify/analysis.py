"""Basic analysis views.

- Expanded Playlist Parking Lot
    - if > 50 tracks, we need multiple requests
    - Discerning between episode and tracks
    - Caching?

TODO: This needs to be reorganized.
"""

import logging
import time
import typing

import httpx
from pydantic import BaseModel

from server import settings

if typing.TYPE_CHECKING:
    from api.models import AppUser


logger = logging.getLogger("spotify_analysis_service")


class Track(BaseModel):
    """Proposed final playlist track."""

    spotify_id: str
    name: str
    duration: int
    artist: "Artist"
    features: "TrackFeatures"
    album: str
    image_url: str


class Playlist(BaseModel):
    """Proposed final playlist."""

    spotify_id: str
    owner: "Owner"

    collaborative: bool
    public: bool

    version: str
    spotify_link: str
    follower_count: int
    track_count: int

    images: list[str]

    description: str | None = None

    tracks: list["Track"]


class Owner(BaseModel):
    """Deserialized Spotify playlist owner.

    Spotify API URL: /users/{user_id}
    """

    spotify_id: str
    image_url: str
    follower_count: int

    # NOTE: This is a nullable field
    display_name: str | None = None


class TrackFeatures(BaseModel):
    """Deserialized Spotify track features."""

    acousticness: float
    danceability: float
    duration: int
    energy: float
    instrumentalness: float
    key: int  # TODO: Pitch class notation enum
    liveness: float
    loudness: float
    mode: int  # 0 or 1 for major or minor
    speechiness: float
    tempo: float  # BPM
    time_signature: int  # 3 - 7 all over 4
    valence: float


class Artist(BaseModel):
    """Artist model.

    Spotify API URL: /artists/{artist_id}

    We need artist information for each track for genres.
    """

    spotify_id: str
    name: str
    genres: list[str]
    image_url: str


class SpotifyAnalysisService:
    """Spotify analysis service."""

    def get_all_playlists(self, user: "AppUser") -> typing.Iterable[dict]:
        """Get all playlists for a user.

        The maximum limit is 50.
        """
        next = f"{settings.SPOTIFY_BASE_URL}me/playlists"

        while next:
            response = httpx.get(
                url=next,
                params={"limit": 50},
                headers={"Authorization": f"Bearer {user.access_token}"},
            )

            if response.is_error:
                raise Exception(response.text)

            resp = response.json()
            next = resp.get("next")

            yield from resp.get("items")

    def get_playlist_tracks(
        self, spotify_id: str, user: "AppUser"
    ) -> typing.Iterable[dict]:
        """Get all tracks for a playlist."""
        next = f"{settings.SPOTIFY_BASE_URL}playlists/{spotify_id}/tracks"
        while next:
            response = httpx.get(
                url=next,
                headers={"Authorization": f"Bearer {user.access_token}"},
            )

            if response.is_error:
                raise Exception(response.text)

            resp = response.json()
            next = resp.get("next")

            yield from resp.get("items")

    def get_playlist(self, spotify_id: str, user: "AppUser") -> dict:
        """Get an individual playlist by spotify ID."""
        with httpx.Client(base_url=settings.SPOTIFY_BASE_URL) as client:
            response = client.get(
                url=f"/playlists/{spotify_id}",
                headers={"Authorization": f"Bearer {user.access_token}"},
            )

            if response.is_error:
                raise Exception(response.text)

            resp = response.json()

            client.close()

        return resp

    def get_artist(self, artist_id: str, user: "AppUser") -> dict:
        """Get artist information."""
        with httpx.Client(base_url=settings.SPOTIFY_BASE_URL) as client:
            response = client.get(
                url=f"/artists/{artist_id}",
                headers={"Authorization": f"Bearer {user.access_token}"},
            )

            if response.is_error:
                raise Exception(response.text)

            resp = response.json()

            client.close()

        return resp

    # TODO: Remove
    def _get_playlist_tracks(
        self, spotify_id: str, user: "AppUser"
    ) -> typing.Iterable[list[dict]]:
        """Get all tracks for a playlist.

        If there are more than 50 tracks we need to continue to make requests.
        """
        initial_url = f"/playlists/{spotify_id}/tracks"
        url = initial_url

        with httpx.Client(base_url=settings.SPOTIFY_BASE_URL) as client:
            while url:
                response = client.get(
                    url=url,
                    headers={"Authorization": f"Bearer {user.access_token}"},
                )

                if response.is_error:
                    raise Exception(response.text)

                resp = response.json()

                client.close()

                url = resp.get("next")

                yield resp.get("items")

    def get_track_features(
        self,
        track_id: str,
        user: "AppUser",
    ) -> dict:
        """Get audio features."""
        with httpx.Client(base_url=settings.SPOTIFY_BASE_URL) as client:
            response = client.get(
                url=f"/audio-features/{track_id}",
                headers={"Authorization": f"Bearer {user.access_token}"},
            )

            if response.is_error:
                raise Exception(response.text)

            resp = response.json()

            client.close()

            return resp

    def get_track_features_batch(
        self,
        track_ids: list[str],
        user: "AppUser",
    ) -> list[dict]:
        """Get audio features for a batch of tracks."""
        with httpx.Client(base_url=settings.SPOTIFY_BASE_URL) as client:
            response = client.get(
                url="/audio-features",
                params={"ids": ",".join(track_ids)},
                headers={"Authorization": f"Bearer {user.access_token}"},
            )

            if response.is_error:
                raise Exception(response.text)

            resp = response.json()

            client.close()

            return resp.get("audio_features", [])

    def get_artist_batch(self, artist_ids: list[str], user: "AppUser") -> list[dict]:
        """Get artist information for a batch of artists."""
        with httpx.Client(base_url=settings.SPOTIFY_BASE_URL) as client:
            response = client.get(
                url="/artists",
                params={"ids": ",".join(artist_ids)},
                headers={"Authorization": f"Bearer {user.access_token}"},
            )

            if response.is_error:
                raise Exception(response.text)

            resp = response.json()

            client.close()

            return resp.get("artists", [])

    def get_playlist_owner(self, user_id: str, user: "AppUser") -> dict:
        """Get owner profile."""
        with httpx.Client(base_url=settings.SPOTIFY_BASE_URL) as client:
            response = client.get(
                url=f"/users/{user_id}",
                headers={"Authorization": f"Bearer {user.access_token}"},
            )

            if response.is_error:
                raise Exception(response.text)

            resp = response.json()

            client.close()

            return resp

    # TODO: Remove
    def expand_playlist(self, spotify_id: str, user: "AppUser") -> Playlist:
        """Expand a playlist to include all tracks and features."""
        playlist = self.get_playlist(spotify_id, user)
        time.sleep(0.5)
        owner = self.get_playlist_owner(playlist.get("owner", {}).get("id"), user)

        data = {
            "spotify_id": playlist.get("id"),
            "owner": Owner(
                **{
                    "spotify_id": owner.get("id"),
                    "image_url": owner.get("images", [{}])[0].get("url"),
                    "follower_count": owner.get("followers", {}).get("total"),
                    "display_name": owner.get("display_name"),
                }
            ),
            "collaborative": playlist.get("collaborative"),
            "public": playlist.get("public"),
            "version": playlist.get("snapshot_id"),
            "spotify_link": playlist.get("external_urls", {}).get("spotify"),
            "follower_count": playlist.get("followers", {}).get("total"),
            "track_count": playlist.get("tracks", {}).get("total"),
            "images": [image.get("url") for image in playlist.get("images", [])],
            "description": playlist.get("description"),
            "tracks": [],  # NOTE: This starts as a map of track id to track data
        }

        expanded_playlist = Playlist.model_construct(**data)

        for tracks in self._get_playlist_tracks(spotify_id, user):
            # Tracks is at most 50 items
            for track in tracks:
                # We're only getting the first artist for now
                id = track.get("track", {}).get("id")

                artist_id = track.get("track", {}).get("artists", [{}])[0].get("id")
                artist_data = self.get_artist(artist_id, user)
                artist = Artist(
                    **{
                        "spotify_id": artist_id,
                        "name": artist_data.get("name"),
                        "genres": artist_data.get("genres"),
                        "image_url": artist_data.get("images", [{}])[0].get("url"),
                    }
                )

                feature_data = self.get_track_features(id, user)
                feature = TrackFeatures(
                    **{
                        "acousticness": float(feature_data.get("acousticness", 0)),
                        "danceability": float(feature_data.get("danceability", 0)),
                        "duration": feature_data.get("duration_ms"),
                        "energy": float(feature_data.get("energy", 0)),
                        "instrumentalness": float(
                            feature_data.get("instrumentalness", 0)
                        ),
                        "key": feature_data.get("key", 0),
                        "liveness": float(feature_data.get("liveness", 0)),
                        "loudness": float(feature_data.get("loudness", 0)),
                        "mode": feature_data.get("mode", 0),
                        "speechiness": float(feature_data.get("speechiness", 0)),
                        "tempo": float(feature_data.get("tempo", 0)),
                        "time_signature": feature_data.get("time_signature", 0),
                        "valence": float(feature_data.get("valence", 0)),
                    }  # type: ignore
                )

                expanded_playlist.tracks.append(
                    Track(
                        **{
                            "spotify_id": id,
                            "name": track.get("track", {}).get("name"),
                            "duration": track.get("track", {}).get("duration_ms"),
                            "album": track.get("track", {})
                            .get("album", {})
                            .get("name"),
                            "image_url": track.get("track", {})
                            .get("album", {})
                            .get("images", [{}])[0]
                            .get("url"),
                            "artist": artist,
                            "features": feature,
                        }
                    )
                )

        return Playlist(**expanded_playlist.model_dump())
