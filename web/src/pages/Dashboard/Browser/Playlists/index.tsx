/**
 * Playlists Dashboard Browser Page
 */

import React, { useCallback, useEffect, useState } from "react";
import { FilterForm } from "./filters/form";
import { BrowserPlaylistPagination } from "./filters/pagination";
import { Table } from "./table";
import { useTokenStore } from "@/store";
import { usePlaylistFilters } from "@/store/filters";
import { useMutation, useQuery } from "@tanstack/react-query";
import { useSavedCounts } from "@/libs/hooks";
import { Breadcrumbs } from "@/components/common/breadcrumbs";

interface BrowserCardProps {
  title: string;
  helpText: string;
  content?: string;
  children?: React.ReactNode;
}

type PlaylistMetadata = {
  total_synced: number;
  total_analyzed: number;
  total_tracks: number;
};

export function BrowserCard({
  title,
  helpText,
  content,
  children,
}: BrowserCardProps) {
  return (
    <article className="bg-white border-t border-emerald-500 flex flex-col gap-2">
      <header className="text-lg p-4 pb-2">{title}</header>
      <section className="px-4 py-2 border-y text-2xl font-semibold font-titles align-middle">
        {content ? (
          content
        ) : children ? (
          children
        ) : (
          <p className="text-gray-500">No content</p>
        )}
      </section>
      <footer className="text-xs text-gray-500 px-4 pb-2 align-middle">
        {helpText}
      </footer>
    </article>
  );
}

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
      <section data-testid="search-bar" className="p-4 bg-white">
        <i className="i-ri-search-line" />
      </section>
      <Breadcrumbs />
      <section className="md:grid md:grid-cols-2 lg:grid-cols-4 divide-x">
        <BrowserCard
          title="Total Playlists"
          helpText="The number of playlists saved in your spotify library."
        >
          {counts.isLoading ? (
            <i className="i-ri-loader-line animate-spin" />
          ) : counts.isError ? (
            <span className="text-rose-500 font-medium">
              Something went wrong
            </span>
          ) : counts.data ? (
            <span className="text-emerald-500 font-medium">
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
            <span className="text-rose-500 font-medium">
              Something went wrong
            </span>
          ) : metadata.data ? (
            <span className="text-emerald-500 font-medium">
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
            <span className="text-rose-500 font-medium">
              Something went wrong
            </span>
          ) : metadata.data ? (
            <span className="text-emerald-500 font-medium">
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
            <span className="text-rose-500 font-medium">
              Something went wrong
            </span>
          ) : metadata.data ? (
            <span className="text-emerald-500 font-medium">
              {metadata.data.total_tracks}
            </span>
          ) : null}
        </BrowserCard>
      </section>
      <main
        data-testid="table"
        className="bg-white flex flex-col flex-1 overflow-auto"
      >
        <header className="p-4 flex items-center justify-between border-y border-t-emerald-500">
          <div>
            <h2 className="text-lg">Table</h2>
            <p>Table Content</p>
          </div>
          <div>
            <button
              className={[
                "bg-white text-emerald-500",
                "border-emerald-500 border",
                "flex items-center px-4 py-2 text-sm",
                "shadow rounded",
                "hover:bg-emerald-500 hover:text-white",
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
