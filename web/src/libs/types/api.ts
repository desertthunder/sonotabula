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

export type Auth = {
  message: string;
  token: string;
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

export enum CountKey {
  Artists = "artists",
  Albums = "albums",
  Tracks = "tracks",
  Playlists = "playlists",
  Shows = "shows",
}

export const COUNT_KEYS: CountKey[] = [
  CountKey.Artists,
  CountKey.Albums,
  CountKey.Tracks,
  CountKey.Playlists,
  CountKey.Shows,
] as const;

export type LibraryCounts = { [key in CountKey]: number };
export type LibraryCountsResponse = { data: LibraryCounts };

/**
 * Browser Types
 */
export type PlaylistTrackFeatures = {
  danceability: number;
  energy: number;
  key: number;
  loudness: number;
  mode: number;
  speechiness: number;
  acousticness: number;
  instrumentalness: number;
  liveness: number;
  valence: number;
  tempo: number;
  duration_ms: number;
  time_signature: number;
};

type ComputedKey = keyof Omit<
  PlaylistTrackFeatures,
  "duration_ms" | "time_signature" | "key" | "mode"
>;
export type PlaylistComputations = {
  superlatives: Record<
    ComputedKey,
    {
      min: number;
      min_track_id: string;
      max: number;
      max_track_id: string;
    }
  >;
  averages: Record<ComputedKey, number>;
  count: {
    key: Record<number, number>;
    mode: Record<number, number>;
    time_signature: Record<number, number>;
  };
};

export type PlaylistTrack = {
  id: string;
  album_id: string;
  name: string;
  spotify_id: string;
  duration: number;
  spotify_url: string;
  features: PlaylistTrackFeatures | null;
  album_name: string | null;
  album_art: string | null;
};

export type BrowserPlaylist = {
  id: string;
  name: string;
  spotify_url: string;
  is_synced: boolean;
  is_analyzed: boolean;
  description: string | null;
  owner_id: string | null;
  version: string | null;
  image_url: string | null;
  public: boolean | null;
  shared: boolean | null;
};

export type BrowserPlaylistResponse = {
  data: {
    playlist: BrowserPlaylist;
    tracks: PlaylistTrack[];
    computations: PlaylistComputations;
  };
  paginator: {
    total: number;
    per_page: number;
    current_page: number;
  };
};
