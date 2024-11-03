import { useMutation } from "@tanstack/react-query";

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
