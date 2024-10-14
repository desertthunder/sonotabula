import type { Auth, FetchError } from "@/libs/types";
import { QueryClient, useQuery, UseQueryOptions } from "@tanstack/react-query";
import type { LoaderFunction, Params } from "react-router-dom";
import { useToken } from "./query";
type PlaylistTracks = {
  playlist: Record<string, string>;
  tracks: Array<Record<string, string>>;
};
export function playlistTracksQuery(
  id: string,
  token: string | null
): UseQueryOptions<PlaylistTracks, FetchError> {
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
    const auth = client.getQueryData<Auth>(["token"]);

    if (!auth) {
      throw new Error("Token not found");
    }

    const query = playlistTracksQuery(params.id as string, auth.token);
    const data = client.getQueryData(query.queryKey);

    if (data) {
      return data;
    }

    return await client.fetchQuery(query);
  };
}

export function usePlaylistTracks(id: string) {
  const { token } = useToken();
  const query = useQuery(playlistTracksQuery(id, token));

  return query;
}
