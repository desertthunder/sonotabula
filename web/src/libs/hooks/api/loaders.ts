import type { FetchError } from "@/libs/types";
import { QueryClient, useQuery, UseQueryOptions } from "@tanstack/react-query";
import type { LoaderFunction, Params } from "react-router-dom";
import { useTokenStore } from "@/store";

export type PlaylistTracks = {
  playlist: Record<string, string>;
  tracks: Array<Record<string, string>>;
};

export function playlistTracksQuery(
  id: string,
  token: string | null
): UseQueryOptions<PlaylistTracks, FetchError> {
  if (!token) {
    throw new Error("Token is required to fetch playlist tracks");
  }

  return {
    queryKey: ["playlist", id],
    queryFn: async () => {
      const response = await fetch(`/api/browser/playlist/${id}/tracks`, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error("Failed to fetch playlist tracks");
      }
      const data = await response.json();
      return data["data"];
    },
  };
}

export function playlistTracksLoader(
  client: QueryClient
): LoaderFunction<PlaylistTracks> {
  return async function ({ params }: { params: Params }) {
    const token = useTokenStore((state) => state.token);

    if (!token) {
      throw new Error("Token is required to fetch playlist tracks");
    }

    const query = playlistTracksQuery(params.id as string, token);
    const data = client.getQueryData(query.queryKey);

    if (data) {
      return data;
    }

    return await client.fetchQuery(query);
  };
}

export function usePlaylistTracks(id: string) {
  const token = useTokenStore((state) => state.token);
  const query = useQuery(playlistTracksQuery(id, token));

  return query;
}
