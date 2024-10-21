import { BrowserKey, CountKey, LibraryKey } from "@libs/types";

export type LibraryPlaylist = {
  spotify_id: string;
  name: string;
  owner_id: string;
  link: string;
  image_url: string;
  num_tracks: number;
  is_synced: boolean;
  description?: string;
};

export type LibraryAlbum = {
  spotify_id: string;
  name: string;
  artist_name: string;
  artist_id: string;
  release_date: string;
  total_tracks: number;
  image_url: string;
};

export type LibraryTrack = {
  spotify_id: string;
  name: string;
  artist_name: string;
  artist_id: string;
  album_name: string;
  album_id: string;
  duration_ms: number;
  link: string;
};

export type LibraryArtist = {
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

export type LibraryResource<T extends LibraryKey> =
  T extends LibraryKey.LibraryPlaylists
    ? LibraryPlaylist[]
    : T extends LibraryKey.LibraryTracks
    ? LibraryTrack[]
    : T extends LibraryKey.LibraryAlbums
    ? LibraryAlbum[]
    : T extends LibraryKey.LibraryArtists
    ? LibraryArtist[]
    : never;

export type LibraryResourceType<T extends LibraryKey> =
  T extends LibraryKey.LibraryPlaylists
    ? LibraryPlaylist
    : T extends LibraryKey.LibraryTracks
    ? LibraryTrack
    : T extends LibraryKey.LibraryAlbums
    ? LibraryAlbum
    : T extends LibraryKey.LibraryArtists
    ? LibraryArtist
    : never;

export type BrowserResource<T extends BrowserKey> =
  T extends BrowserKey.BrowserPlaylists
    ? BrowserPlaylist[]
    : T extends BrowserKey.BrowserTracks
    ? BrowserTrack[]
    : T extends BrowserKey.BrowserAlbums
    ? BrowserAlbum[]
    : T extends BrowserKey.BrowserArtists
    ? LibraryArtist[]
    : never;

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

export type ComputedKey = keyof Omit<
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

export type BrowserPlaylistTrack = {
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

export type BrowserPlaylistResponse = {
  data: {
    playlist: BrowserPlaylist;
    tracks: BrowserPlaylistTrack[];
    computations: PlaylistComputations;
  };
};

export type Pagination = {
  total: number;
  per_page: number;
  page: number;
  num_pages: number;
};

export type BrowserAlbum = {
  id: string;
  name: string;
  artists: {
    id: string;
    name: string;
    spotify_id: string;
  }[];
  spotify_id: string;
  release_year: number;
  image_url?: string | null;
};

export type BrowserTrack = {
  id: string;
  name: string;
  spotify_id: string;
  duration: number;
  album_id: string;
  album_name: string;
  album_art: string;
  spotify_url: string;
  is_synced: boolean;
  is_analyzed: boolean;
};

export type BrowserPlaylist = {
  id: string;
  spotify_id: string;
  name: string;
  is_synced: boolean;
  is_analyzed: boolean;
  description?: string;
  owner_id?: string;
  version?: string;
  image_url?: string;
  public?: boolean;
  shared?: boolean;
};

export type ListeningHistoryItem = {
  id: string;
  played_at: string;
  track: {
    spotify_id: string;
    name: string;
    duration: number;
  };
  album: {
    spotify_id: string;
    name: string;
    release_date: string;
    image_url: string;
  };
  artists: {
    spotify_id: string;
    name: string;
  }[];
  image_url: string;
};
