import { authService } from "@libs/services";
import React from "react";
import { useNavigate } from "react-router-dom";

function onClickSignup() {
  authService.login();
}

export default function Signup() {
  const navigate = useNavigate();

  React.useEffect(() => {
    const cachedToken = localStorage.getItem("token");

    if (!cachedToken) {
      return;
    }

    async function validateToken() {
      if (!cachedToken) {
        return;
      }

      const isValid = await authService.validateToken(cachedToken);

      if (!isValid) {
        localStorage.removeItem("token");

        navigate("/login");
      } else {
        navigate("/dashboard");
      }
    }

    validateToken();
  }, [navigate]);

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
