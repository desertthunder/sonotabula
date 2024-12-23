import type {
  FetchError,
  ListeningHistoryItem,
  BrowserPlaylist,
  Pagination,
  ProfileResponse,
  PlaylistMetadata,
} from "@libs/types";
import isNil from "lodash/isNil";

export async function fetchListeningHistory(token: string | null) {
  if (!token) {
    throw new Error("No token provided");
  }
  const url = new URL("/server/api/v1/playback/recent", window.location.origin);
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

export async function fetchTokenState(token: string | null) {
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

export async function fetchPlaylistsMetadata(token: string | null) {
  if (!token) {
    throw new Error("No token available");
  }

  const url = new URL(
    "/server/api/v1/browser/playlists/meta",
    window.location.origin
  );

  const response = await fetch(url.toString(), {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch playlists metadata");
  }

  return (await response.json()) as PlaylistMetadata;
}

export async function analyzePage({
  token,
  params,
}: {
  token: string | null;
  params: URLSearchParams;
}) {
  const url = new URL(
    "/server/api/v1/browser/playlists",
    window.location.origin
  );
  url.search = params.toString();

  const response = await fetch(url.toString(), {
    headers: {
      Authorization: `Bearer ${token}`,
    },
    method: "POST",
  });

  return await response.json();
}

export async function fetchPlaylists(
  token: string | null,
  params: URLSearchParams
) {
  const uri = new URL(
    "/server/api/v1/browser/playlists",
    window.location.origin
  );
  uri.search = params.toString();
  const response = await fetch(uri.toString(), {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch playlists");
  }

  return (await response.json()) as {
    data: BrowserPlaylist[];
    pagination: {
      total: number;
      per_page: number;
      page: number;
      num_pages: number;
    };
  };
}

export async function fetchProfile(token: string | null) {
  const url = new URL("api/v1/profile", window.location.origin);

  const response = await fetch(url.href, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch profile");
  }

  return (await response.json()) as ProfileResponse;
}
