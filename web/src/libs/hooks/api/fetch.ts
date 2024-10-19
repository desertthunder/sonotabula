import type { Resource, FetchError, ListeningHistoryItem } from "@libs/types";
import { BASE_URL } from "@libs/services";
import { ResourceKey } from "@libs/types";

export function getEndpoint(resourceKey: string) {
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

export function getBrowserEndpoint(resourceKey: string) {
  switch (resourceKey) {
    case ResourceKey.LibraryPlaylists:
      return `${BASE_URL}/api/browser/playlists`;
    case ResourceKey.LibraryTracks:
      return `${BASE_URL}/api/browser/tracks`;
    case ResourceKey.BrowserAlbums:
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

export async function browserFetcher<T extends ResourceKey>(
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

export async function paginatedBrowserFetcher<T extends ResourceKey>(
  resource: ResourceKey,
  token: string,
  params: { page: number; page_size: number } = {
    page: 1,
    page_size: 10,
  }
): Promise<Resource<T>> {
  const uri = new URL(getBrowserEndpoint(resource));

  uri.searchParams.append("page", params.page.toString());
  uri.searchParams.append("page_size", params.page_size.toString());

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

  return (await response.json()) as Resource<T>;
}

export async function fetchListeningHistory(token: string | null) {
  if (!token) {
    throw new Error("No token provided");
  }
  const res = await fetch("/api/playback/recent/", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!res.ok) {
    const error: FetchError = {
      code: res.status,
      message: res.statusText,
    };

    return Promise.reject(error);
  }

  const data = await res.json();

  return data["data"] as ListeningHistoryItem;
}
