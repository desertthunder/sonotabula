import type { Resource, FetchError, LibraryCountsResponse } from "@libs/types";
import { useQuery, UseQueryResult } from "@tanstack/react-query";
import { useToken } from "./query";
import { BASE_URL } from "@libs/services";
import { ResourceKey } from "@libs/types";

function getEndpoint(resourceKey: string) {
  switch (resourceKey) {
    case ResourceKey.LibraryPlaylists:
      return `${BASE_URL}/api/library/playlists`;
    case ResourceKey.LibraryTracks:
      return `${BASE_URL}/api/library/tracks`;
    case ResourceKey.LibraryAlbums:
      return `${BASE_URL}/api/library/albums`;
    case ResourceKey.LibraryArtists:
      return `${BASE_URL}/api/library/artists`;
    default:
      return BASE_URL;
  }
}

function getBrowserEndpoint(resourceKey: string) {
  switch (resourceKey) {
    case ResourceKey.LibraryPlaylists:
      return `${BASE_URL}/api/browser/playlists`;
    case ResourceKey.LibraryTracks:
      return `${BASE_URL}/api/browser/tracks`;
    case ResourceKey.LibraryAlbums:
      return `${BASE_URL}/api/browser/albums`;
    case ResourceKey.LibraryArtists:
      return `${BASE_URL}/api/browser/artists`;
    default:
      return BASE_URL;
  }
}

export async function fetcher<T extends ResourceKey>(
  resource: ResourceKey,
  token: string,
  limit?: number | null
): Promise<Resource<T>> {
  const uri = new URL(getEndpoint(resource));

  if (limit && limit > 50) {
    uri.searchParams.append("limit", "50");
  } else if (limit) {
    uri.searchParams.append("limit", limit.toString());
  }

  const response = await fetch(uri.toString(), {
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

  return data["data"] as Resource<T>;
}

export function browserFetcher<T extends ResourceKey>(
  resource: ResourceKey,
  token: string
): Promise<Resource<T>> {
  const uri = new URL(getBrowserEndpoint(resource));

  return fetch(uri.toString(), {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  }).then(async (response) => {
    if (!response.ok) {
      return Promise.reject({
        code: response.status,
        message: response.statusText,
      } as FetchError);
    }

    const data = await response.json();

    return data["data"] as Resource<T>;
  });
}

export function useFetch<T extends ResourceKey>(
  resource: ResourceKey,
  limit?: number | null
): UseQueryResult<Resource<T>> {
  const { token, client } = useToken();

  const query = useQuery<Resource<T>>(
    {
      queryKey: [resource],
      queryFn: async () => {
        if (!token) {
          throw new Error("Token not found");
        }

        return await fetcher<T>(resource, token, limit);
      },
    },
    client
  );

  return query;
}

export function useBrowse<T extends ResourceKey>(
  resource: ResourceKey
): UseQueryResult<Resource<T>> {
  const { token, client } = useToken();

  const query = useQuery<Resource<T>>(
    {
      queryKey: [resource],
      queryFn: async () => {
        if (!token) {
          throw new Error("Token not found");
        }

        return await browserFetcher<T>(resource, token);
      },
    },
    client
  );

  return query;
}

export function useSavedCounts() {
  const { token, client } = useToken();

  const query = useQuery(
    {
      queryKey: ["saved-counts"],
      queryFn: async () => {
        if (!token) {
          throw new Error("Token not found");
        }

        const response = await fetch(`${BASE_URL}/api/data/saved`, {
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
