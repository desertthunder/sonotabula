import { LibraryKey } from "@libs/types/enums";

export function getLibraryEndpoint(resourceKey: string) {
  switch (resourceKey) {
    case LibraryKey.LibraryPlaylists:
      return `/api/library/playlists`;
    case LibraryKey.LibraryTracks:
      return `/api/library/tracks`;
    case LibraryKey.LibraryAlbums:
      return `/api/library/albums`;
    case LibraryKey.LibraryArtists:
      return `/api/library/artists`;
    default:
      throw new Error("Invalid resource key");
  }
}

export function getBrowserEndpoint(resourceKey: string) {
  switch (resourceKey) {
    case LibraryKey.LibraryPlaylists:
      return `/api/browser/playlists`;
    case LibraryKey.LibraryTracks:
      return `/api/browser/tracks`;
    case LibraryKey.LibraryAlbums:
      return `/api/browser/albums`;
    case LibraryKey.LibraryArtists:
      return `/api/browser/artists`;
    default:
      throw new Error("Invalid resource key");
  }
}

export function getSavedEndpoint() {
  return `/api/data/saved`;
}
