import { useSearch } from "wouter";

export function useQueryParams() {
  const params = useSearch();
  const search = new URLSearchParams();

  for (const [key, value] of params.split("&").map((pair) => pair.split("="))) {
    search.set(key, value);
  }

  return search;
}
