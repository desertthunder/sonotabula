import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";

function useQueryParams(): Record<string, string> {
  const location = useLocation();
  const params = new URLSearchParams(location.search);

  return Object.fromEntries(params.entries());
}

export default function Dashboard() {
  const params = useQueryParams();
  const navigate = useNavigate();

  const query = useQuery({
    queryKey: ["token"],
    queryFn: async () => {
      console.debug("Checking token validity");

      const token = params.token || localStorage.getItem("token");

      if (!token) {
        throw new Error("Token not found");
      }

      const response = await fetch("/api/validate", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error("Token invalid");
      }

      return response.json();
    },
    refetchInterval: 5 * 60 * 1000, // 5 minutes
  });

  React.useEffect(() => {
    if (query.isError) {
      navigate("/login");
    } else if (query.isSuccess && params.token) {
      navigate("/dashboard");
    }
  }, [query, navigate, params]);

  return (
    <div>
      <h1>Dashboard</h1>
      <p>Check your browser's local storage to see the token.</p>
    </div>
  );
}
