import {
  FetchError,
  LibraryCountsResponse,
  Resource,
  ResourceKey,
} from "@/libs/types";
import {
  QueryClient,
  useQuery,
  useQueryClient,
  UseQueryResult,
} from "@tanstack/react-query";
import { useMemo } from "react";
import { useLocation } from "react-router-dom";
import { browserFetcher, fetcher } from "./fetch";
import { BASE_URL } from "@/libs/services";

export function useQueryParams(): Record<string, string> {
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

  const query = useQuery(
    {
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
      retry: false,
      refetchInterval: 5 * 60 * 1000, // 5 minutes
    },
    queryClient
  );

  return { query, token };
}

export function useFetch<T extends ResourceKey>(
  resource: ResourceKey,
  limit?: number | null
): UseQueryResult<Resource<T>> {
  const { token, client } = useToken();

  const query = useQuery<Resource<T>>(
    {
      queryKey: [resource],
      queryFn: async () => {
        if (!token) {
          throw new Error("Token not found");
        }

        return await fetcher<T>(resource, token, limit);
      },
    },
    client
  );

  return query;
}

export function useBrowse<T extends ResourceKey>(
  resource: ResourceKey
): UseQueryResult<Resource<T>> {
  const { token, client } = useToken();

  const query = useQuery<Resource<T>>(
    {
      queryKey: [`${resource}-browser`],
      queryFn: async () => {
        if (!token) {
          throw new Error("Token not found");
        }

        return await browserFetcher<T>(resource, token);
      },
    },
    client
  );

  return query;
}

export function useSavedCounts() {
  const { token, client } = useToken();

  const query = useQuery(
    {
      queryKey: ["saved-counts"],
      queryFn: async () => {
        if (!token) {
          throw new Error("Token not found");
        }

        const response = await fetch(`${BASE_URL}/api/data/saved`, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          return Promise.reject({
            code: response.status,
            message: response.statusText,
          } as FetchError);
        }

        const data = (await response.json()) as LibraryCountsResponse;

        return data["data"];
      },
    },
    client
  );

  return query;
}
