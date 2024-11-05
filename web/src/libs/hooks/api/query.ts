/**
 * @todo paginate queries
 */
import { useTokenStore } from "@/store";
import {
  BrowserPlaylistResponse,
  Endpoints,
  FetchError,
  LibraryCountsResponse,
  ListeningHistoryItem,
} from "@libs/types";
import { QueryClient, useQuery, useQueryClient } from "@tanstack/react-query";
import { useCallback, useEffect } from "react";
import { useSearch } from "wouter";
import {
  checkToken,
  fetchBrowserPlaylists,
  fetchLibraryPlaylistTracks,
  fetchListeningHistory,
} from "./fetch";

export function useQueryParams(): Record<string, string> {
  const [search] = useSearch();
  const params = new URLSearchParams(search);

  return Object.fromEntries(params.entries());
}

export function useTokenValidator() {
  const params = useQueryParams();
  const queryClient = useQueryClient();
  const token = useTokenStore((state) => state.token);
  const setToken = useTokenStore((state) => state.setToken);

  useEffect(() => {
    if (params.token) {
      setToken(params.token);
    }
  }, [params.token, setToken]);

  const query = useQuery(
    {
      queryKey: ["token"],
      queryFn: async () => {
        if (!token) {
          throw new Error("Token not found");
        }

        const url = new URL("/server/api/validate", window.location.origin);

        const response = await fetch(url.toString(), {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          throw new Error("Token invalid");
        }

        const data: { message: string; token: string } = await response.json();

        return data;
      },
      retry: false,
      refetchInterval: 5 * 60 * 1000, // 5 minutes
    },
    queryClient
  );

  return query;
}

export function useSavedCounts() {
  const token = useTokenStore((state) => state.token);
  const client = useQueryClient();

  const query = useQuery(
    {
      queryKey: ["saved-counts"],
      queryFn: async () => {
        if (!token) {
          throw new Error("Token not found");
        }

        const endpoint = new URL(Endpoints.Saved, window.location.origin);

        const response = await fetch(endpoint.toString(), {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          return Promise.reject({
            code: response.status,
            message: response.statusText,
          } as FetchError);
        }

        const data = (await response.json()) as LibraryCountsResponse;

        return data["data"];
      },
    },
    client
  );

  return query;
}

export function usePlaylistTracks(id: string) {
  const token = useTokenStore((state) => state.token);
  const client = useQueryClient();
  const query = useQuery(
    {
      queryKey: ["playlist", id],
      queryFn: async () => {
        const response = await fetch(
          `/server/api/browser/playlist/${id}/tracks`,
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (!response.ok) {
          throw new Error("Failed to fetch playlist tracks");
        }

        return (await response.json()) as BrowserPlaylistResponse;
      },
    },
    client
  );

  return query;
}

export function useListeningHistory() {
  const token = useTokenStore((s) => s.token);

  const query = useQuery<ListeningHistoryItem, FetchError>({
    queryKey: ["listeningHistory"],
    queryFn: async () => {
      return await fetchListeningHistory(token);
    },
    retry: 2,
  });

  return query;
}

export function useCheckToken() {
  const token = useTokenStore((s) => s.token);

  const query = useQuery({
    queryKey: ["checkToken"],
    queryFn: () => checkToken(token),
    staleTime: Infinity,
  });

  return query;
}

export function useBrowserPlaylists(
  {
    page = 1,
    pageSize = 10,
    sortBy,
    filters,
  }: {
    page?: number;
    pageSize?: number;
    sortBy?: string;
    filters?: string[][];
  },
  client: QueryClient
) {
  const token = useTokenStore((s) => s.token);
  const query = useQuery(
    {
      queryKey: ["browser-playlists", page],
      queryFn: async () =>
        await fetchBrowserPlaylists({ page, pageSize, token, sortBy, filters }),
    },
    client
  );

  return query;
}

export async function useLibraryPlaylistTracks(playlist_id: string) {
  const token = useTokenStore((s) => s.token);

  const query = useQuery({
    queryKey: ["library_playlist_tracks", playlist_id],
    queryFn: () => fetchLibraryPlaylistTracks(playlist_id, token),
  });

  const handler = useCallback(
    (playlist_id: string) => {
      return fetchLibraryPlaylistTracks(playlist_id, token);
    },
    [token]
  );

  return {
    query,
    handler,
  };
}
