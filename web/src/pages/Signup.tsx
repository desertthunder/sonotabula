import { useMutation } from "@tanstack/react-query";
import { useTokenValidator } from "@/libs/hooks";
import { useLocation } from "wouter";
import { useCallback, useEffect } from "react";

export default function Signup() {
  const [, navigate] = useLocation();
  const query = useTokenValidator();

  // Login
  const mutation = useMutation({
    mutationFn: async () => {
      const response = await fetch("/api/login", {
        method: "POST",
        headers: {},
      });

      if (!response.ok) {
        throw new Error("Login failed");
      }

      return response.json();
    },
  });

  useEffect(() => {
    if (query.isSuccess) {
      navigate("/dashboard");
    } else if (query.isError) {
      console.error(query.error);
    }
  }, [query.isSuccess, query.isError, query.error, navigate]);

  useEffect(() => {
    if (mutation.isSuccess) {
      navigate("/dashboard");
    } else if (mutation.isError) {
      console.error(mutation.error);
    }
  }, [mutation.isSuccess, mutation.isError, mutation.error, navigate]);

  const onClickSignup = useCallback(() => {
    mutation.mutate();
  }, [mutation]);

  return (
    <main className="container min-h-80">
      <h1 className="text-5xl font-semibold font-headings">
        Spotify Dashboard
      </h1>
      <div className="m-4 font-prose">Signup card</div>
      <button
        onClick={onClickSignup}
        className="bg-primary text-white font-semibold py-2 px-4 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50"
      >
        Sign Up
      </button>
    </main>
  );
}
