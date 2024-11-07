"""Service layer.

TODO - Create a base module for the RedirectURI base class.

TODO - Move the params class to the params module in the spotify service
module.
"""

from api.services.spotify.auth import SpotifyAuthService
from api.services.spotify.data import SpotifyDataService
from api.services.spotify.library import SpotifyLibraryService
from api.services.spotify.playback import SpotifyPlaybackService

DATA = SpotifyDataService()
AUTH = SpotifyAuthService()
LIBRARY = SpotifyLibraryService()
PLAYBACK = SpotifyPlaybackService()
