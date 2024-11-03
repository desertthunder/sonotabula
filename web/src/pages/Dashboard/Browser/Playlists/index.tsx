/**
 * Playlists Dashboard Browser Page
 */

import { useCallback, useEffect, useState } from "react";
import { FilterForm } from "./filters/form";
import { BrowserPlaylistPagination } from "./filters/pagination";
import { Table } from "./table";
import { useTokenStore } from "@/store";
import { usePlaylistFilters } from "@/store/filters";
import { useMutation, useQuery, UseQueryResult } from "@tanstack/react-query";
import { useSavedCounts } from "@/libs/hooks";
import { Breadcrumbs, BrowserCard, SearchBar } from "@/components/common";
import { LibraryCounts } from "@/libs/types";

type PlaylistMetadata = {
  total_synced: number;
  total_analyzed: number;
  total_tracks: number;
};

async function AnalyzePage({
  token,
  params,
}: {
  token: string | null;
  params: URLSearchParams;
}) {
  const url = new URL(
    "/server/api/v1/browser/playlists",
    window.location.origin
  );
  url.search = params.toString();

  const response = await fetch(url.toString(), {
    headers: {
      Authorization: `Bearer ${token}`,
    },
    method: "POST",
  });

  return await response.json();
}

async function fetchPlaylistsMetadata(token: string | null) {
  if (!token) {
    throw new Error("No token available");
  }

  const url = new URL(
    "/server/api/v1/browser/playlists/meta",
    window.location.origin
  );

  const response = await fetch(url.toString(), {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch playlists metadata");
  }

  return (await response.json()) as PlaylistMetadata;
}

function usePlaylistsMetadata() {
  const token = useTokenStore((state) => state.token);
  const query = useQuery({
    queryKey: ["browser", "playlists", "metadata"],
    queryFn: () => fetchPlaylistsMetadata(token),
  });

  return query;
}

function usePageAnalysisMutation() {
  const token = useTokenStore((state) => state.token);
  const getParams = usePlaylistFilters((state) => state.getAllParams);

  const mutation = useMutation({
    mutationFn: () => AnalyzePage({ token, params: getParams() }),
  });

  return mutation;
}

function BrowserCards({
  metadata,
  counts,
}: {
  metadata: UseQueryResult<PlaylistMetadata>;
  counts: UseQueryResult<LibraryCounts>;
}) {
  return (
    <section className="md:grid md:grid-cols-2 lg:grid-cols-4 divide-x">
      <BrowserCard
        title="Total Playlists"
        helpText="The number of playlists saved in your spotify library."
      >
        {counts.isLoading ? (
          <i className="i-ri-loader-line animate-spin" />
        ) : counts.isError ? (
          <span className="text-error font-medium">Something went wrong</span>
        ) : counts.data ? (
          <span className="text-primary font-medium">
            {counts.data.playlists}
          </span>
        ) : null}
      </BrowserCard>
      <BrowserCard
        title="Synced Playlists"
        helpText="The number of playlists synced with your spotify account."
      >
        {metadata.isLoading ? (
          <i className="i-ri-loader-line animate-spin" />
        ) : metadata.isError ? (
          <span className="text-error font-medium">Something went wrong</span>
        ) : metadata.data ? (
          <span className="text-primary font-medium">
            {metadata.data.total_synced}
          </span>
        ) : null}
      </BrowserCard>
      <BrowserCard
        title="Analyzed"
        helpText="The number of playlists analyzed for recommendations."
      >
        {metadata.isLoading ? (
          <i className="i-ri-loader-line animate-spin" />
        ) : metadata.isError ? (
          <span className="text-error font-medium">Something went wrong</span>
        ) : metadata.data ? (
          <span className="text-primary font-medium">
            {metadata.data.total_analyzed}
          </span>
        ) : null}
      </BrowserCard>
      <BrowserCard
        title="Total Tracks"
        helpText="The number of tracks in your synced playlists."
      >
        {metadata.isLoading ? (
          <i className="i-ri-loader-line animate-spin" />
        ) : metadata.isError ? (
          <span className="text-error font-medium">Something went wrong</span>
        ) : metadata.data ? (
          <span className="text-primary font-medium">
            {metadata.data.total_tracks}
          </span>
        ) : null}
      </BrowserCard>
    </section>
  );
}

export function PlaylistsBrowser() {
  const [isLoading, setIsLoading] = useState(false);
  const counts = useSavedCounts();
  const metadata = usePlaylistsMetadata();
  const mutation = usePageAnalysisMutation();

  const handleAnalyzePageClick = useCallback(() => {
    setIsLoading(true);
    mutation.mutate();
  }, [mutation]);

  useEffect(() => {
    const timeout = setTimeout(() => {
      if (mutation.isPending) return;

      setIsLoading(false);
    }, 1500);

    return () => {
      clearTimeout(timeout);
    };
  }, [mutation.isPending]);

  return (
    <div className="flex flex-col w-full text-sm min-h-min">
      <SearchBar />
      <Breadcrumbs context="playlists" />
      <BrowserCards metadata={metadata} counts={counts} />
      <main
        data-testid="table"
        className="bg-white flex flex-col flex-1 overflow-auto"
      >
        <header className="p-4 flex items-center justify-between border-y border-t-primary">
          <div>
            <h2 className="text-lg">Table</h2>
            <p>Table Content</p>
          </div>
          <div>
            <button
              className={[
                "bg-white text-primary",
                "border-primary border",
                "flex items-center px-4 py-2 text-sm",
                "shadow rounded",
                "hover:bg-primary hover:text-white",
                isLoading ? "cursor-wait pointer-events-none" : "",
              ].join(" ")}
              disabled={isLoading}
              onClick={handleAnalyzePageClick}
            >
              {isLoading ? (
                <i className="i-ri-loader-line animate-spin" />
              ) : (
                <span>Analyze Page</span>
              )}
            </button>
          </div>
        </header>
        <FilterForm />
        <Table />
      </main>
      <BrowserPlaylistPagination />
    </div>
  );
}
