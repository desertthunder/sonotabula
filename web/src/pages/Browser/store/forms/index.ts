import { create } from "zustand";

// Filter Form State
//
// See api/filters/playlist.py for the server-side filterset
//
// Numeric Comparison Filters
export enum NumericFilter {
  TracksGreaterThan = "num_tracks_gt",
  TracksLessThan = "num_tracks_lt",
}

export enum BooleanFilter {
  Private = "private",
  Analyzed = "is_analyzed",
  MyPlaylists = "my_playlists",
  Shared = "shared",
}

// i.e. searchable fields
export enum StringFilter {
  Name = "name",
  Description = "description",
  TrackName = "track_name", // This is a special case for track search
}

export enum PaginationType {
  Page = "page",
  PageSize = "page_size",
}

export type PlaylistFilterState = {
  [NumericFilter.TracksGreaterThan]: number | null;
  [NumericFilter.TracksLessThan]: number | null;
  [BooleanFilter.Private]: boolean;
  [BooleanFilter.Analyzed]: boolean;
  [BooleanFilter.MyPlaylists]: boolean;
  [StringFilter.Name]: string;
  [StringFilter.Description]: string;
  [StringFilter.TrackName]: string;
  [PaginationType.Page]: number;
  [PaginationType.PageSize]: number;
};

export const usePlaylistFilterStore = create<PlaylistFilterState>()((_set) => ({
  [NumericFilter.TracksGreaterThan]: null,
  [NumericFilter.TracksLessThan]: null,
  [BooleanFilter.Private]: false,
  [BooleanFilter.Shared]: false,
  [BooleanFilter.Analyzed]: false,
  [BooleanFilter.MyPlaylists]: false,
  [StringFilter.Name]: "",
  [StringFilter.Description]: "",
  [StringFilter.TrackName]: "",
  [PaginationType.Page]: 1,
  [PaginationType.PageSize]: 10,
}));

export const stateToQueryParams = (state: PlaylistFilterState) => {
  const params = new URLSearchParams();

  Object.entries(state).forEach(([key, value]) => {
    if (value !== null && value !== "") {
      params.append(key, value.toString());
    }
  });

  return params;
};
