import { useMutation } from "@tanstack/react-query";
import { useTokenStore } from "@/store";

export type TaskArgs = {
  pid: string | undefined;
  operation: "sync" | "analyze";
  token: string | null;
};

export async function callTask({ pid, operation, token }: TaskArgs) {
  if (!token) {
    throw new Error("No token available");
  }

  if (!pid) {
    throw new Error("No playlist id available");
  }

  const url = new URL(`/api/v1/browser/playlists/${pid}`, window.location.href);

  const res = await fetch(url.toString(), {
    method: "PATCH",
    body: JSON.stringify({ operation }),
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  });

  if (!res.ok) {
    throw new Error(`Failed to ${operation} playlist`);
  }

  return await res.json();
}

export function usePlaylistAction(
  playlist_id: string | undefined,
  operation: "sync" | "analyze"
) {
  const token = useTokenStore((state) => state.token);

  return useMutation({
    mutationKey: ["playlist", operation, playlist_id],
    mutationFn: () => callTask({ pid: playlist_id, operation, token }),
  });
}
