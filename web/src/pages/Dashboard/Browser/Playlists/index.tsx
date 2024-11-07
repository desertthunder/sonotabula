/**
 * Playlists Dashboard Browser Page
 */

import { useCallback, useEffect, useState } from "react";
import { FilterForm } from "./filters/form";
import { BrowserPlaylistPagination } from "./filters/pagination";
import { Table } from "./table";
import { UseQueryResult } from "@tanstack/react-query";
import { usePlaylistsMetadata, useSavedCounts } from "@/libs/hooks";
import { Breadcrumbs, BrowserCard } from "@/components/common";
import { LibraryCounts, PlaylistMetadata } from "@/libs/types";
import { usePageAnalysisMutation, usePlaylistsQuery } from "@/libs/hooks";

function PlaylistBrowserCards({
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
  const query = usePlaylistsQuery();

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
      <Breadcrumbs context="playlists" />
      <PlaylistBrowserCards metadata={metadata} counts={counts} />
      <main
        data-testid="table"
        className="bg-white flex flex-col flex-1 overflow-auto"
      >
        <header className="p-4 flex items-center justify-between border-y border-t-primary">
          <h2 className="text-lg">Table</h2>
          <FilterForm />
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
        </header>
        <Table context={query} />
      </main>
      <BrowserPlaylistPagination />
    </div>
  );
}
