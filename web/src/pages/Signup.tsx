import { useTokenStore } from "@/store";
import { useMutation, useQuery } from "@tanstack/react-query";
import { useCallback, useEffect } from "react";
import { useLocation } from "wouter";

async function checkToken(token: string | null) {
  if (!token) {
    console.debug("No token found");

    return null;
  }

  try {
    const response = await fetch("/api/validate", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (response.status >= 500) {
      throw new Error(
        `Server error: ${response.status} ${response.statusText}`
      );
    } else if (!response.ok) {
      console.debug(
        `Failed to validate token: ${response.status} ${response.statusText}`
      );

      return null;
    }

    const data = await response.json();

    console.debug(data.message);

    return data;
  } catch (error) {
    console.error(error);

    return null;
  }
}

export default function Signup() {
  const token = useTokenStore((s) => s.token);
  const [, setLocation] = useLocation();
  const query = useQuery({
    queryKey: ["checkToken"],
    queryFn: () => checkToken(token),
    staleTime: Infinity,
  });

  useEffect(() => {
    if (query.isSuccess && query.data?.token) {
      setTimeout(() => {
        setLocation("/dashboard");
      }, 2500);
    }

    return () => {
      query.refetch();
    };
  }, [query, setLocation]);

  const mutation = useMutation({
    mutationFn: async () => {
      const response = await fetch("/api/login", {
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

  useEffect(() => {
    if (mutation.isSuccess && mutation.data?.redirect) {
      window.location.href = mutation.data.redirect;

      return;
    } else if (mutation.isError) {
      console.error(mutation.error);
    }
  }, [mutation.data, mutation.error, mutation.isSuccess, mutation.isError]);

  const onClickSignup = useCallback(async () => {
    mutation.mutate();
  }, [mutation]);

  return (
    <main className="container min-h-80 flex items-center justify-center">
      <div className="w-full max-w-xl p-6 space-y-8 sm:p-8 bg-primary text-white drop-shadow-xl rounded-lg shadow">
        <header className="flex justify-between flex-col gap-4 text-5xl font-bold">
          <h1 className="text-left">
            <i className="i-ri-spotify-fill text-5xl align-middle mr-2"></i>
            <span className="align-middle">Dashspot</span>
          </h1>
          <p className="text-sm text-gray-100 font-medium">
            Dashspot is a library manager and analytics tool for your music
            library.
          </p>
        </header>

        <button
          type="button"
          onClick={onClickSignup}
          className={[
            "group",
            "w-full px-5 py-3",
            "text-base font-medium text-center text-primary",
            "bg-gray-100 rounded-lg hover:bg-white",
            "transition-colors duration-300",
            "focus:ring-4 focus:ring-primary-300 sm:w-auto",
            "flex items-center justify-center gap-x-2",
            mutation.isPending || query.isLoading
              ? "cursor-wait pointer-events-none"
              : "",
          ].join(" ")}
        >
          <i
            className={[
              "text-primary text-xl",
              "group-hover:rotate-45 group-hover:scale-110 ",
              "transition-transform duration-300",
              mutation.isPending || query.isLoading
                ? "animate-spin i-ri-loader-4-fill"
                : "i-ri-music-2-fill",
            ].join(" ")}
          ></i>
          <span>
            {query.isLoading
              ? "Checking token..."
              : mutation.isPending
              ? "Logging in..."
              : "Login"}
          </span>
        </button>
      </div>
    </main>
  );
}
