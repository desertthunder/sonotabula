import { create } from "zustand";

export type FilterKeys = "name" | "my_playlists" | "is_analyzed" | "private";

type PlaylistFilterState = {
  page: number;
  pageSize: number;
  total: number;
  isFetching: boolean;
  filters: Map<FilterKeys, string>;
};

const defaultState: PlaylistFilterState = {
  page: 1,
  pageSize: 10,
  total: 0,
  isFetching: false,
  filters: new Map(),
} as const;

interface PlaylistFilterActions {
  getAllParams: () => URLSearchParams;
  updatePageSize: (pageSize: number) => void;
  updateTotal: (total: number) => void;
  setPage: (page: number) => void;
  nextPage: () => void;
  previousPage: () => void;
  updateFetching: (isFetching: boolean) => void;
  reset: () => void;
}

export const usePlaylistFilters = create<
  PlaylistFilterState & PlaylistFilterActions
>()((set, get) => ({
  ...defaultState,
  getAllParams: () => {
    const { page, pageSize, filters } = get();

    const params = new URLSearchParams();

    params.set("page", page.toString());
    params.set("page_size", pageSize.toString());

    for (const [key, value] of filters) {
      params.set(key, value);
    }

    return params;
  },
  reset: () => {
    set(() => defaultState);
  },
  updateFetching: (isFetching: boolean) => {
    set(() => ({ isFetching }));
  },
  updateTotal: (total: number) => {
    set(() => ({ total }));
  },
  setPage: (page: number) => {
    set((state) => {
      if (page < 1) {
        return state;
      } else if (page * state.pageSize > state.total) {
        return state;
      } else {
        return { page };
      }
    });
  },
  updatePageSize: (pageSize: number) => {
    set(() => ({ pageSize }));
  },
  nextPage: () => {
    set((state) => {
      if (state.page * state.pageSize >= state.total) {
        return state;
      }

      return { page: state.page + 1 };
    });
  },
  previousPage: () => {
    set((state) => {
      if (state.page === 1) {
        return state;
      }

      return { page: state.page - 1 };
    });
  },
}));

export function setFilters(key: FilterKeys, value: string) {
  return usePlaylistFilters.setState((state) => {
    const filters = new Map(state.filters);

    filters.set(key, value);

    return { filters };
  });
}

export function removeFilter(key: FilterKeys) {
  return usePlaylistFilters.setState((state) => {
    const filters = new Map(state.filters);

    if (!filters.has(key)) return state;

    filters.delete(key);

    return { filters };
  });
}
