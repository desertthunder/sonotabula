import { BASE_URL } from "@libs/services";
import { ResourceKey } from "@libs/types";

export function getEndpoint(resourceKey: string) {
  switch (resourceKey) {
    case ResourceKey.LibraryPlaylists:
      return `${BASE_URL}/api/library/playlists`;
    case ResourceKey.LibraryTracks:
      return `${BASE_URL}/api/library/tracks`;
    case ResourceKey.LibraryAlbums:
      return `${BASE_URL}/api/library/albums`;
    case ResourceKey.LibraryArtists:
      return `${BASE_URL}/api/library/artists`;
    default:
      return BASE_URL;
  }
}

export function getBrowserEndpoint(resourceKey: string) {
  switch (resourceKey) {
    case ResourceKey.LibraryPlaylists:
      return `${BASE_URL}/api/browser/playlists`;
    case ResourceKey.LibraryTracks:
      return `${BASE_URL}/api/browser/tracks`;
    case ResourceKey.LibraryAlbums:
      return `${BASE_URL}/api/browser/albums`;
    case ResourceKey.LibraryArtists:
      return `${BASE_URL}/api/browser/artists`;
    default:
      return BASE_URL;
  }
}
