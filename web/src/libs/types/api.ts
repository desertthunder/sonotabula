export type Playlist = {
  spotify_id: string;
  name: string;
  owner_id: string;
  link: string;
  image_url: string;
  num_tracks: number;
  description?: string;
};

export type Album = {
  spotify_id: string;
  name: string;
  artist_name: string;
  artist_id: string;
  release_date: string;
  total_tracks: number;
  image_url: string;
};

export type Track = {
  spotify_id: string;
  name: string;
  artist_name: string;
  artist_id: string;
  album_name: string;
  album_id: string;
  duration_ms: number;
  link: string;
};

export type Artist = {
  genres: string[];
  spotify_id: string;
  name: string;
  link: string;
  image_url: string;
};

export type FetchError = {
  code: number;
  message: string;
};

export enum ResourceKey {
  LibraryPlaylists = "library-playlists",
  LibraryTracks = "library-tracks",
  LibraryAlbums = "library-albums",
  LibraryArtists = "library-artists",
}

export const RESOURCE_KEYS = [
  ResourceKey.LibraryPlaylists,
  ResourceKey.LibraryTracks,
  ResourceKey.LibraryAlbums,
  ResourceKey.LibraryArtists,
] as const;

export type Resource<T extends ResourceKey> =
  T extends ResourceKey.LibraryPlaylists
    ? Playlist[]
    : T extends ResourceKey.LibraryTracks
    ? Track[]
    : T extends ResourceKey.LibraryAlbums
    ? Album[]
    : T extends ResourceKey.LibraryArtists
    ? Artist[]
    : never;
