export enum CountKey {
  Artists = "artists",
  Albums = "albums",
  Tracks = "tracks",
  Playlists = "playlists",
  Shows = "shows",
}

export enum LibraryKey {
  LibraryPlaylists = "library-playlists",
  LibraryTracks = "library-tracks",
  LibraryAlbums = "library-albums",
  LibraryArtists = "library-artists",
}

export enum BrowserKey {
  BrowserPlaylists = "browser-playlists",
  BrowserTracks = "browser-tracks",
  BrowserAlbums = "browser-albums",
  BrowserArtists = "browser-artists",
}

export enum NumericFilterType {
  TracksGreaterThan = "num_tracks_gt",
  TracksLessThan = "num_tracks_lt",
}

export enum BooleanFilterType {
  Private = "private",
  Analyzed = "is_analyzed",
  MyPlaylists = "my_playlists",
  Shared = "shared",
}

// i.e. searchable fields
export enum StringFilterType {
  Name = "name",
  Description = "description",
  TrackName = "track_name",
}

export enum PaginationType {
  Page = "page",
  PageSize = "page_size",
}

export enum Routes {
  Home = "/",
  Signup = "/signup",
  Login = "/login",
  Dashboard = "/dashboard",
}
