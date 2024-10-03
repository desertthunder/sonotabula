import React from "react";
import { redirect } from "react-router-dom";

export function useToken() {
  const [token, setToken] = React.useState<string>();

  React.useEffect(() => {
    const tok = localStorage.getItem("token");

    return () => {
      if (tok) {
        setToken(tok);
      } else {
        redirect("/signup");
      }
    };
  }, []);

  return token;
}

export default function Home() {
  useToken();

  return (
    <main>
      <h1 className="text-5xl font-semibold">Spotify Dashboard</h1>
      <div className="m-4">Home page</div>
    </main>
  );
}
