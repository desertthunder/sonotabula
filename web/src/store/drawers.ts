import { BrowserKey, LibraryKey } from "@libs/types";
import has from "lodash/has";
import { create } from "zustand";

export type DrawerKey = `${LibraryKey}-${string}` | `${BrowserKey}-${string}`;

export type DrawerState = {
  drawers: Record<DrawerKey, boolean>;
};

export interface DrawerActions {
  register: (id: DrawerKey) => void;
  registerBatch: (ids: DrawerKey[]) => void;
  isRegistered?: (id: DrawerKey) => boolean;

  openDrawer: (id: DrawerKey) => void;
  closeDrawer: (id: DrawerKey) => void;
  toggleDrawer: (id: DrawerKey) => void;
  isDrawerOpen: (id: DrawerKey) => boolean;
}

export const useDrawerStore = create<DrawerState & DrawerActions>()(
  (set, get) => ({
    drawers: {},
    isRegistered: (id) => has(get().drawers, id),
    register: (id) => {
      set((old) => {
        return {
          ...old,
          drawers: {
            ...old.drawers,
            [id]: false,
          },
        };
      });
    },
    registerBatch: (ids: DrawerKey[]) => {
      const merge: Record<DrawerKey, boolean> = {};

      ids.forEach((id) => {
        merge[id] = false;
      });

      const old = get();

      return {
        ...old,
        drawers: {
          ...old.drawers,
          ...merge,
        },
      };
    },
    openDrawer: (id) =>
      set((old) => {
        // Close all other drawers
        // We don't want to mutate the original state object
        const state: DrawerState = { ...old };

        for (const drawerId of Object.keys(old.drawers)) {
          state.drawers[drawerId as DrawerKey] = false;
        }

        return {
          drawers: { ...state.drawers, [id]: true },
        };
      }),
    closeDrawer: (id) =>
      set((state) => ({
        drawers: { ...state.drawers, [id]: false },
      })),

    toggleDrawer: (id) =>
      set((state) => ({
        drawers: { ...state.drawers, [id]: !state.drawers[id] },
      })),

    isDrawerOpen: (id) => get().drawers[id] || false,
  })
);
