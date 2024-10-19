import { useQuery } from "@tanstack/react-query";
import { useTokenStore } from "@/store";
import isNil from "lodash/isNil";
import { useCallback } from "react";

export async function getPlaylistTracks(
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

export async function usePlaylistTracks(playlist_id: string) {
  const token = useTokenStore((s) => s.token);

  const query = useQuery({
    queryKey: ["library_playlist_tracks", playlist_id],
    queryFn: () => getPlaylistTracks(playlist_id, token),
  });

  return query;
}

export function usePlaylistTracksHandler() {
  const token = useTokenStore((s) => s.token);

  return useCallback(
    (playlist_id: string) => getPlaylistTracks(playlist_id, token),
    [token]
  );
}
