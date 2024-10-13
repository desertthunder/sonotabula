import { useNavigate } from "react-router-dom";
import { useMutation } from "@tanstack/react-query";
import { useTokenValidator } from "@/libs/hooks";

// TODO: Create a proper index page
export default function Signup() {
  const navigate = useNavigate();
  const { query } = useTokenValidator();

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

  function onClickSignup() {
    mutation.mutate();
  }

  if (query.isSuccess) {
    navigate("/dashboard");
  } else if (query.isError) {
    console.error(query.error);
  }

  if (mutation.isSuccess) {
    window.location.href = mutation.data.redirect;
  } else if (mutation.isError) {
    console.error(mutation.error);
  }

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
