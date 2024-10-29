/**
 * @description Types for index Dashboard page
 */

type ArtistTuple = [string, string];

type PlaylistTrack = {
  spotify_id: string;
  name: string;
  album_id: string;
  album_name: string;
  album_type: string;
  artists: ArtistTuple[];
  duration_ms: number;
  isrc: string;
};

export type Playlist = {
  spotify_id: string;
  collaborative: boolean;
  description: string;
  spotify_link: string;
  image_url: string;
  name: string;
  owner: string[];
  public: boolean;
  snapshot_id: string;
  follower_count: number;
  id: string;
  tracks: PlaylistTrack[];
};
