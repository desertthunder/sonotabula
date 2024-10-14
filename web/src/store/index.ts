import { create } from "zustand";
import { persist } from "zustand/middleware";

export interface State {
  token: string | null;
  setToken: (token: string) => void;
}

export const useTokenStore = create<State>()(
  persist(
    (set, _get) => ({
      token: null,
      setToken: (token: string) => set({ token }),
    }),
    {
      name: "token-storage",
    }
  )
);
