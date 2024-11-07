import { create } from "zustand";

export type FilterKeys = "name" | "my_playlists" | "is_analyzed" | "private";

export type PlaylistFilterState = {
  total: number;
  isFetching: boolean;
};

const defaultState: PlaylistFilterState = {
  total: 0,
  isFetching: false,
} as const;

interface PlaylistFilterActions {
  updateTotal: (total: number) => void;
  updateFetching: (isFetching: boolean) => void;
}

export const usePlaylistFilters = create<
  PlaylistFilterState & PlaylistFilterActions
>()((set, _get) => ({
  ...defaultState,
  updateFetching: (isFetching: boolean) => {
    set(() => ({ isFetching }));
  },
  updateTotal: (total: number) => {
    set(() => ({ total }));
  },
}));
