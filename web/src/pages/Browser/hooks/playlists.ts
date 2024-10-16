import { FetchError } from "@/libs/types";
import { useTokenStore } from "@/store";
import { QueryClient, useQuery } from "@tanstack/react-query";
import type { Pagination } from "./shared";

type Playlist = {
  id: string;
  spotify_id: string;
  name: string;
  is_synced: boolean;
  is_analyzed: boolean;
  description?: string;
  owner_id?: string;
  version?: string;
  image_url?: string;
  public?: boolean;
  shared?: boolean;
};

export async function fetchPlaylists({
  page = 1,
  pageSize = 10,
  token,
  sortBy,
  filters,
}: {
  token: string | null;
  page?: number;
  pageSize?: number;
  sortBy?: string;
  filters?: string;
}) {
  const url = new URL("/api/browser/playlists", window.location.origin);
  url.searchParams.append("page", page.toString());
  url.searchParams.append("page_size", pageSize.toString());

  if (sortBy) {
    url.searchParams.append("sortBy", sortBy);
  }

  if (filters) {
    url.searchParams.append("filters", filters);
  }

  const response = await fetch(url.toString(), {
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

  const data = await response.json();

  return data as { data: Playlist[]; pagination: Pagination };
}

export function usePlaylists(
  {
    page = 1,
    pageSize = 10,
    sortBy,
    filters,
  }: {
    page?: number;
    pageSize?: number;
    sortBy?: string;
    filters?: string;
  },
  client: QueryClient
) {
  const token = useTokenStore((s) => s.token);
  const query = useQuery(
    {
      queryKey: ["browser-playlists", page],
      queryFn: async () =>
        await fetchPlaylists({ page, pageSize, token, sortBy, filters }),
    },
    client
  );

  return query;
}
