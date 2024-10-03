import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { authService } from "@/libs/services";

function useQueryParams(): Record<string, string> {
  const location = useLocation();
  const params = new URLSearchParams(location.search);

  return Object.fromEntries(params.entries());
}

export default function Dashboard() {
  const params = useQueryParams();
  const navigate = useNavigate();
  const [token, setToken] = React.useState<string | null>(null);
  const delay = 60;

  React.useEffect(() => {
    const cachedToken = localStorage.getItem("token");

    if (!params.token && !cachedToken) {
      navigate("/login");

      return;
    }

    if (!params.token && cachedToken) {
      const interval = setInterval(async () => {
        console.debug("Checking token validity");

        const isValid = await authService.validateToken(cachedToken);

        if (!isValid) {
          clearInterval(interval);

          localStorage.removeItem("token");

          navigate("/login");
        } else {
          setToken(cachedToken);
        }
      }, delay * 1000);

      return () => clearInterval(interval);
    }
  }, [navigate, params, delay]);

  React.useEffect(() => {
    if (!token) {
      return;
    }

    console.debug("Token (state) changed");
  }, [token]);

  return (
    <div>
      <h1>Dashboard</h1>
      <p>Check your browser's local storage to see the token.</p>
    </div>
  );
}
