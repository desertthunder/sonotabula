import { create } from "zustand";
import {
  NumericFilterType,
  BooleanFilterType,
  StringFilterType,
  PaginationType,
} from "@libs/types";

// Filter Form State
//
// See api/filters/playlist.py for the server-side filterset
export type PlaylistFilterState = {
  [NumericFilterType.TracksGreaterThan]: number | null;
  [NumericFilterType.TracksLessThan]: number | null;
  [BooleanFilterType.Private]: boolean;
  [BooleanFilterType.Analyzed]: boolean;
  [BooleanFilterType.MyPlaylists]: boolean;
  [StringFilterType.Name]: string;
  [StringFilterType.Description]: string;
  [StringFilterType.TrackName]: string;
  [PaginationType.Page]: number;
  [PaginationType.PageSize]: number;
};

export const usePlaylistFilterStore = create<PlaylistFilterState>()((_set) => ({
  [NumericFilterType.TracksGreaterThan]: null,
  [NumericFilterType.TracksLessThan]: null,
  [BooleanFilterType.Private]: false,
  [BooleanFilterType.Shared]: false,
  [BooleanFilterType.Analyzed]: false,
  [BooleanFilterType.MyPlaylists]: false,
  [StringFilterType.Name]: "",
  [StringFilterType.Description]: "",
  [StringFilterType.TrackName]: "",
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
