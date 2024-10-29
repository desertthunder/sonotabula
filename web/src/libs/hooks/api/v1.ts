/**
 * @module api/v1
 *
 * @description Incremental re-implementations of queries & mutations.
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
 * @description Fetches library tracks.
 */
export async function fetchLibraryTracks(
  token: string | null,
  params: LibraryParams
) {
  const uri = new URL("/api/v1/library/tracks", window.location.origin);
  uri.searchParams.append("page", params.page.toString());
  uri.searchParams.append("page_size", params.page_size.toString());

  const response = await fetch(uri.toString(), {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch library tracks.");
  }

  return (await response.json()) as LibraryResponse<LibraryKey.LibraryTracks>;
}

export async function fetchLibraryAlbums(
  token: string | null,
  params: LibraryParams
) {
  const uri = new URL("/api/v1/library/albums", window.location.origin);
  uri.searchParams.append("page", params.page.toString());
  uri.searchParams.append("page_size", params.page_size.toString());

  const response = await fetch(uri.toString(), {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch library albums.");
  }

  return (await response.json()) as LibraryResponse<LibraryKey.LibraryAlbums>;
}

export async function syncLibraryPlaylists(
  token: string | null,
  params: LibraryParams
) {
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
    throw new Error("Failed to sync library playlists.");
  }

  return await response.json();
}

export async function syncLibraryTracks(
  token: string | null,
  params: LibraryParams
) {
  const uri = new URL("/api/v1/library/tracks", window.location.origin);
  uri.searchParams.append("page", params.page.toString());
  uri.searchParams.append("page_size", params.page_size.toString());

  const response = await fetch(uri.toString(), {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error("Failed to sync library tracks.");
  }

  return await response.json();
}

/**
 * @description A hook to select & dispatch API request to fetch library data.
 */
export function useLibraryData<T extends LibraryKey>(
  scope: T,
  params: LibraryParams
) {
  const token = useTokenStore((state) => state.token);

  const searchParams = new URLSearchParams();
  searchParams.append("page", params.page.toString());
  searchParams.append("page_size", params.page_size.toString());

  const query = useQuery({
    queryKey: [scope, searchParams.toString()],
    queryFn: async () => {
      switch (scope) {
        case LibraryKey.LibraryPlaylists:
          return await fetchLibraryPlaylists(token, params);
        case LibraryKey.LibraryTracks:
          return await fetchLibraryTracks(token, params);
        case LibraryKey.LibraryAlbums:
          return await fetchLibraryAlbums(token, params);
        default:
          throw new Error("Invalid scope");
      }
    },
    refetchInterval: false,
  });

  return query;
}

export function useSync(scope: LibraryKey, params: LibraryParams) {
  const token = useTokenStore((state) => state.token);

  const searchParams = new URLSearchParams();
  searchParams.append("page", params.page.toString());
  searchParams.append("page_size", params.page_size.toString());

  const mutation = useMutation({
    mutationKey: [scope, searchParams.toString()],
    mutationFn: async (_args?: string[]) => {
      switch (scope) {
        case LibraryKey.LibraryPlaylists:
          return await syncLibraryPlaylists(token, params);
        case LibraryKey.LibraryTracks:
          return await syncLibraryTracks(token, params);
        default:
          throw new Error("Invalid scope");
      }
    },
  });

  return mutation as UseMutationResult<any>;
}
