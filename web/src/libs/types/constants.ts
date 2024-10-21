/**
 * @todo: Change to production URL.
 *
 * This is the Django server URL.
 * */
export const BASE_URL = "http://localhost:8000";

import {
  CountKey,
  LibraryKey,
  NumericFilterType,
  BooleanFilterType,
  StringFilterType,
  BrowserKey,
} from "@libs/types";

export const Counts: CountKey[] = [
  CountKey.Artists,
  CountKey.Albums,
  CountKey.Tracks,
  CountKey.Playlists,
  CountKey.Shows,
] as const;

export const LibraryKeys = [
  LibraryKey.LibraryPlaylists,
  LibraryKey.LibraryTracks,
  LibraryKey.LibraryAlbums,
  LibraryKey.LibraryArtists,
] as const;

export const BrowserKeys = [
  BrowserKey.BrowserPlaylists,
  BrowserKey.BrowserTracks,
  BrowserKey.BrowserAlbums,
  BrowserKey.BrowserArtists,
] as const;

export const numericalFilters: [NumericFilterType, string][] = [
  [NumericFilterType.TracksGreaterThan, "Tracks Greater Than"],
  [NumericFilterType.TracksLessThan, "Tracks Less Than"],
] as const;

export const booleanFilters: [BooleanFilterType, string][] = [
  [BooleanFilterType.Private, "Private"],
  [BooleanFilterType.Analyzed, "Analyzed"],
  [BooleanFilterType.MyPlaylists, "My Playlists"],
] as const;

export const stringFilters: [StringFilterType, string][] = [
  [StringFilterType.Name, "Name"],
  [StringFilterType.Description, "Description"],
] as const;

export const LibraryTitles = {
  [LibraryKey.LibraryPlaylists]: "Playlists",
  [LibraryKey.LibraryTracks]: "Tracks",
  [LibraryKey.LibraryAlbums]: "Albums",
  [LibraryKey.LibraryArtists]: "Artists",
} as const;
