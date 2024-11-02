import { BrowserKey, CountKey, LibraryKey } from "@libs/types/enums";

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
  image_url: string;
  is_synced: boolean;
  is_analyzed: boolean;
};

export type LibraryArtist = {
  genres: string[];
  spotify_id: string;
  name: string;
  link: string;
  image_url: string;
  is_synced: boolean;
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

// Browser Types

export type Superlative = {
  min: number;
  min_track_id: string;
  max: number;
  max_track_id: string;
};

export type TrackFeatures = {
  id: string;
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
  TrackFeatures,
  "duration_ms" | "time_signature" | "key" | "mode"
>;
export type Superlatives = {
  danceability: Superlative;
  energy: Superlative;
  loudness: Superlative;
  speechiness: Superlative;
  acousticness: Superlative;
  instrumentalness: Superlative;
  liveness: Superlative;
  valence: Superlative;
  tempo: Superlative;
  duration_ms: Superlative;
};
export type Computations = {
  // superlatives: Record<ComputedKey, Superlative>;
  // averages: Record<ComputedKey, number>;
  // count: {
  //   key: Record<number, number>;
  //   mode: Record<number, number>;
  //   time_signature: Record<number, number>;
  // };
  superlatives: Superlatives;
  averages: {
    danceability: number;
    energy: number;
    loudness: number;
    speechiness: number;
    acousticness: number;
    instrumentalness: number;
    liveness: number;
    valence: number;
    tempo: number;
    duration_ms: number;
  };
  count: {
    key: Record<string, number>;
    mode: Record<string, number>;
    time_signature: Record<string, number>;
  };
};

export type BrowserPlaylistDetail = {
  id: string;
  name: string;
  spotify_url: string;
  num_tracks: number;
  is_synced: boolean;
  is_analyzed: boolean;
  description: string;
  owner_id: string;
  version: string;
  image_url: string;
  public: boolean;
  shared: boolean;
};

export type BrowserPlaylistTrack = {
  id: string;
  album_id: string;
  name: string;
  spotify_id: string;
  duration: number;
  spotify_url: string;
  features: TrackFeatures;
  album_name: string;
  album_art: string;
  artists: {
    id: string;
    name: string;
    spotify_id: string;
  }[];
};

export type BrowserPlaylistResponse = {
  data: {
    playlist: BrowserPlaylistDetail;
    tracks: BrowserPlaylistTrack[];
    computations: Computations | null;
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
