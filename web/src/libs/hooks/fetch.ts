import { useQuery, UseQueryResult } from "@tanstack/react-query";
import { useToken } from "./query";
import { BASE_URL } from "@libs/services";
import type { Playlist, Track, Album, Artist } from "@libs/types/api";

type FetchError = {
  code: number;
  message: string;
};

export enum ResourceKey {
  LibraryPlaylists = "library-playlists",
  LibrarySongs = "library-songs",
  LibraryTracks = "library-tracks",
  LibraryAlbums = "library-albums",
  LibraryArtists = "library-artists",
}

export const RESOURCE_KEYS = [
  ResourceKey.LibraryPlaylists,
  ResourceKey.LibraryTracks,
  ResourceKey.LibraryAlbums,
  ResourceKey.LibraryArtists,
] as const;

type Resource<T extends ResourceKey> = T extends ResourceKey.LibraryPlaylists
  ? Playlist[]
  : T extends ResourceKey.LibraryTracks
  ? Track[]
  : T extends ResourceKey.LibraryAlbums
  ? Album[]
  : T extends ResourceKey.LibraryArtists
  ? Artist[]
  : never;

function getEndpoint(resourceKey: string) {
  switch (resourceKey) {
    case ResourceKey.LibraryPlaylists:
      return `${BASE_URL}/api/library/playlists`;
    case ResourceKey.LibrarySongs:
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
