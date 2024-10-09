export type Playlist = {
  spotify_id: string;
  name: string;
  owner_name: string;
  owner_id: string;
  link: string;
  image_url: string;
  num_tracks: number;
  track_link: string;
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
