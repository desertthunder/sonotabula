import { useCheckToken, useLoginMutation } from "@libs/hooks";
import { useCallback, useEffect } from "react";
import { useLocation } from "wouter";

export default function Signup() {
  const [, setLocation] = useLocation();
  const query = useCheckToken();
  const mutation = useLoginMutation();

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

  useEffect(() => {
    if (mutation.isSuccess && mutation.data?.redirect) {
      window.location.href = mutation.data.redirect;

      return;
    }
  }, [mutation.data, mutation.isSuccess, mutation.isError]);

  const onClickSignup = useCallback(async () => {
    mutation.mutate();
  }, [mutation]);

  return (
    <main className="container min-h-80 flex items-center justify-center">
      <div className="w-full max-w-xl p-6 space-y-8 sm:p-8 bg-primary text-white drop-shadow-xl rounded-lg shadow">
        <header className="flex justify-between flex-col gap-4 text-5xl font-bold">
          <h1 className="text-left">
            <i className="i-ri-spotify-fill text-5xl align-middle mr-2"></i>
            <span className="align-middle">Sonotabula</span>
          </h1>
          <p className="text-sm text-gray-100 font-medium">
            Sonotabula is a library manager and analytics tool for your music
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
