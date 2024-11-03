import { LibraryKey } from "@libs/types/enums";

export function getLibraryEndpoint(resourceKey: string) {
  switch (resourceKey) {
    case LibraryKey.LibraryPlaylists:
      return `/server/api/library/playlists`;
    case LibraryKey.LibraryTracks:
      return `/server/api/library/tracks`;
    case LibraryKey.LibraryAlbums:
      return `/server/api/library/albums`;
    case LibraryKey.LibraryArtists:
      return `/server/api/library/artists`;
    default:
      throw new Error("Invalid resource key");
  }
}

export function getBrowserEndpoint(resourceKey: string) {
  switch (resourceKey) {
    case LibraryKey.LibraryPlaylists:
      return `/server/api/browser/playlists`;
    case LibraryKey.LibraryTracks:
      return `/server/api/browser/tracks`;
    case LibraryKey.LibraryAlbums:
      return `/server/api/browser/albums`;
    case LibraryKey.LibraryArtists:
      return `/server/api/browser/artists`;
    default:
      throw new Error("Invalid resource key");
  }
}

export function getSavedEndpoint() {
  return `/server/api/data/saved`;
}
