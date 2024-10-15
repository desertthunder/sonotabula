import { useOutletContext } from "react-router-dom";

export type BrowserContext = {
  setTitle: (title: string) => void;
  setDescription: (description: string) => void;
};

export function useBrowserContext() {
  return useOutletContext<BrowserContext>();
}

export type Pagination = {
  total: number;
  per_page: number;
  page: number;
};
