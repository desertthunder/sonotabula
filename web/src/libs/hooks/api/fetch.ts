import type {
  LibraryResource,
  FetchError,
  ListeningHistoryItem,
  BrowserPlaylist,
  Pagination,
  BrowserKey,
  BrowserResource,
} from "@libs/types";
import { LibraryKey, getBrowserEndpoint } from "@libs/types";
import isNil from "lodash/isNil";

export async function browserFetcher<T extends LibraryKey>(
  resource: LibraryKey,
  token: string
): Promise<LibraryResource<T>> {
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

    return data["data"] as LibraryResource<T>;
  });
}

export async function paginatedBrowserFetcher<T extends BrowserKey>(
  resource: BrowserKey,
  token: string | null,
  params: { page: number; page_size: number } = {
    page: 1,
    page_size: 10,
  }
): Promise<{
  data: BrowserResource<T>;
  pagination: Pagination;
}> {
  if (!token) {
    throw new Error("No token provided");
  }

  const uri = new URL(getBrowserEndpoint(resource), window.location.origin);

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

  const data = (await response.json()) as {
    data: BrowserResource<T>;
    pagination: Pagination;
  };

  return data;
}

export async function fetchListeningHistory(token: string | null) {
  if (!token) {
    throw new Error("No token provided");
  }
  const url = new URL("/server/api/playback/recent", window.location.origin);
  const res = await fetch(url.toString(), {
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

export async function checkToken(token: string | null) {
  if (!token) {
    return null;
  }

  const url = new URL("/server/api/validate", window.location.origin);

  const response = await fetch(url.toString(), {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (response.status >= 500) {
    throw new Error(`Server error: ${response.status} ${response.statusText}`);
  } else if (!response.ok) {
    throw new Error(
      `Failed to validate token: ${response.status} ${response.statusText}`
    );
  }

  const data = await response.json();

  return data;
}

export async function fetchBrowserPlaylists({
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
  filters?: string[][];
}) {
  const url = new URL("/api/browser/playlists", window.location.origin);
  url.searchParams.append("page", page.toString());
  url.searchParams.append("page_size", pageSize.toString());

  if (sortBy) {
    url.searchParams.append("sort_by", sortBy);
  }

  if (filters && filters.length > 0) {
    filters.forEach(([key, value]) => {
      url.searchParams.append(key, value);
    });
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

  return data as { data: BrowserPlaylist[]; pagination: Pagination };
}

export async function fetchLibraryPlaylistTracks(
  playlist_id: string,
  token?: string | null
) {
  if (isNil(token)) {
    throw new Error("Token is required to fetch playlist tracks");
  }

  const response = await fetch(`/api/library/playlists/${playlist_id}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return (await response.json()) as {
    playlist: Record<string, string>;
    tracks: any[]; // eslint-disable-line
  };
}
