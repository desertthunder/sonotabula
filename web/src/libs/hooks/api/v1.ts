/**
 * @module api/v1
 *
 * @description Incremental re-implementations of queries.
 */
import type { LibraryResourceType } from "@/libs/types";
import { LibraryKey } from "@/libs/types";
import { useTokenStore } from "@/store";
import {
  useMutation,
  UseMutationResult,
  useQuery,
} from "@tanstack/react-query";

export type LibraryParams = {
  total: number;
  page: number;
  page_size: number;
};

export type LibraryResponse<T extends LibraryKey> = {
  data: LibraryResourceType<T>[];
  total: number;
  page: number;
  page_size: number;
};

/**
 * @description Fetches library playlists.
 */
export async function fetchLibraryPlaylists(
  token: string | null,
  params: LibraryParams
) {
  const uri = new URL("/api/v1/library/playlists", window.location.origin);
  uri.searchParams.append("page", params.page.toString());
  uri.searchParams.append("page_size", params.page_size.toString());

  const response = await fetch(uri.toString(), {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch library playlists.");
  }

  return (await response.json()) as LibraryResponse<LibraryKey.LibraryPlaylists>;
}

/**
 * @description A hook to dispatch API request to fetch library playlists.
 */
export function useLibraryPlaylists(scope: LibraryKey, params: LibraryParams) {
  const token = useTokenStore((state) => state.token);

  const searchParams = new URLSearchParams();
  searchParams.append("page", params.page.toString());
  searchParams.append("page_size", params.page_size.toString());

  const query = useQuery({
    queryKey: [scope, searchParams.toString()],
    queryFn: async () => await fetchLibraryPlaylists(token, params),
  });

  return query;
}

export function useSyncPlaylists(scope: LibraryKey, params: LibraryParams) {
  const token = useTokenStore((state) => state.token);

  const searchParams = new URLSearchParams();
  searchParams.append("page", params.page.toString());
  searchParams.append("page_size", params.page_size.toString());

  const mutation = useMutation({
    mutationKey: [scope, searchParams.toString()],
    mutationFn: async (_args?: string[]) => {
      const uri = new URL("/api/v1/library/playlists", window.location.origin);
      uri.searchParams.append("page", params.page.toString());
      uri.searchParams.append("page_size", params.page_size.toString());

      const response = await fetch(uri.toString(), {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error("Failed to sync library.");
      }

      return await response.json();
    },
  });

  return mutation as UseMutationResult<any>;
}
