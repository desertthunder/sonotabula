import { useMutation } from "@tanstack/react-query";
import { useQueryParams } from "..";
import { useTokenStore } from "@/store";

export function useLoginMutation() {
  const mutation = useMutation({
    mutationFn: async () => {
      const uri = new URL("/server/api/login", window.location.origin);
      const response = await fetch(uri, {
        method: "POST",
        headers: {},
      });

      if (!response.ok) {
        throw new Error("Login failed");
      }

      // Pause for 2.5 seconds
      await new Promise((resolve) => setTimeout(resolve, 2500));

      return await response.json();
    },
  });

  return mutation;
}

export function usePageAnalysisMutation() {
  const token = useTokenStore((state) => state.token);
  const params = useQueryParams();
  const mutation = useMutation({
    mutationFn: async () => {
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
    },
  });

  return mutation;
}
