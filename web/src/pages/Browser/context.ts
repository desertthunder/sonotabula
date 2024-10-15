import { useOutletContext } from "react-router-dom";

export type BrowserContext = {
  title: string;
  setTitle: (title: string) => void;
  description: string;
  setDescription: (description: string) => void;
  pagination?: {
    total: number;
    per_page: number;
    page: number;
    count?: number;
  };
  setPagination: (pagination: BrowserContext["pagination"]) => void;
};

export function useBrowserContext() {
  return useOutletContext<BrowserContext>();
}
