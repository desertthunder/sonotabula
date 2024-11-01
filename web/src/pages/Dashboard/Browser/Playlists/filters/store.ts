import { create } from "zustand";

type PlaylistFilterState = {
  page: number;
  pageSize: number;
  total: number;
  isFetching: boolean;
};

interface PlaylistFilterActions {
  updatePageSize: (pageSize: number) => void;
  updateTotal: (total: number) => void;
  setPage: (page: number) => void;
  nextPage: () => void;
  previousPage: () => void;
  updateFetching: (isFetching: boolean) => void;
}

export const usePlaylistFilters = create<
  PlaylistFilterState & PlaylistFilterActions
>()((set, _get) => ({
  page: 1,
  pageSize: 10,
  total: 0,
  isFetching: false,
  updateFetching: (isFetching: boolean) => {
    set(() => ({ isFetching }));
  },
  updateTotal: (total: number) => {
    set(() => ({ total }));
  },
  setPage: (page: number) => {
    set((state) => {
      if (page < 1) return state;

      if (page * state.pageSize > state.total) return state;

      return { page };
    });
  },
  updatePageSize: (pageSize: number) => {
    set(() => ({ pageSize }));
  },
  nextPage: () => {
    set((state) => {
      if (state.page * state.pageSize >= state.total) return state;

      return { page: state.page + 1 };
    });
  },
  previousPage: () => {
    set((state) => {
      if (state.page === 1) return state;

      return { page: state.page - 1 };
    });
  },
}));
