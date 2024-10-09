import { QueryClient, useQuery, useQueryClient } from "@tanstack/react-query";
import { useEffect, useMemo } from "react";
import { useLocation, useNavigate } from "react-router-dom";

function useQueryParams(): Record<string, string> {
  const location = useLocation();
  const params = new URLSearchParams(location.search);

  return Object.fromEntries(params.entries());
}

export function useToken(): {
  token: string | null;
  client: QueryClient;
} {
  const queryClient = useQueryClient();
  const queryData = queryClient.getQueryData<{
    message: string;
    token: string;
  }>(["token"]);

  return {
    token: queryData?.token ?? null,
    client: queryClient,
  };
}

export function useTokenValidator() {
  const navigate = useNavigate();
  const params = useQueryParams();
  const queryClient = useQueryClient();
  const queryData = queryClient.getQueryData<{
    message: string;
    token: string;
  }>(["token"]);

  const token = useMemo(() => {
    if (params.token) {
      return params.token;
    } else {
      return queryData?.token ?? null;
    }
  }, [params.token, queryData]);

  const query = useQuery({
    queryKey: ["token"],
    queryFn: async () => {
      console.debug("Checking token validity");

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

      const data: { message: string; token: string } = await response.json();

      return data;
    },
    refetchInterval: 5 * 60 * 1000, // 5 minutes
  });

  useEffect(() => {
    if (query.isError) {
      navigate("/login");
    } else if (query.isSuccess && params.token) {
      navigate("/dashboard");
    }
  }, [query, navigate, params]);

  return { token, query };
}
