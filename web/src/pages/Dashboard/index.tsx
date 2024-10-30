/**
 * @description index of /dashboard url namespace
 */
import { LibraryParams, useLibraryData, useSync } from "@/libs/hooks/api/v1";
import { Counts, LibraryArtist, LibraryKey } from "@libs/types";
import last from "lodash/last";
import { useCallback, useEffect, useState } from "react";
import { useLocation, useSearch } from "wouter";
import { Drawers } from "./components/drawers";
import { StatCard } from "./components/stats";
import { RealTimeTable } from "./components/tables";
import { Tabs } from "./components/tabs";

const initialParams: LibraryParams = {
  total: 0,
  page: 1,
  page_size: 10,
  last: undefined,
};

/**
 * useQueryUrlParams extracts the query parameters from the URL
 * to determine the current scope of the dashboard table.
 *
 * @returns {LibraryKey}
 */
function useQueryUrlParams(): LibraryKey {
  const search = useSearch();

  if (!search) {
    return LibraryKey.LibraryPlaylists;
  }

  const params = new URLSearchParams(search);
  // We're looking for the `tab` key in the query parameters
  // to determine the current scope of the dashboard table.
  if (!params.get("tab")) {
    return LibraryKey.LibraryPlaylists;
  }

  switch (params.get("tab")) {
    case "tracks":
      return LibraryKey.LibraryTracks;
    case "albums":
      return LibraryKey.LibraryAlbums;
    case "artists":
      return LibraryKey.LibraryArtists;
    default:
      return LibraryKey.LibraryPlaylists;
  }
}

export function Dashboard() {
  const scope = useQueryUrlParams();
  const [pageParams, setPageParams] = useState<LibraryParams>(initialParams);
  const [pageData, setPageData] = useState<LibraryParams>(initialParams);
  const [, setLocation] = useLocation();

  const onTabChange = useCallback(
    (key: LibraryKey) => {
      switch (key) {
        case LibraryKey.LibraryTracks:
          return setLocation("/dashboard?tab=tracks");
        case LibraryKey.LibraryAlbums:
          return setLocation("/dashboard?tab=albums");
        case LibraryKey.LibraryArtists:
          return setLocation("/dashboard?tab=artists");
        case LibraryKey.LibraryPlaylists:
          return setLocation("/dashboard?tab=playlists");
        default:
          return setLocation("/dashboard");
      }
    },
    [setLocation]
  );

  const next = () => {
    setPageParams({
      ...pageParams,
      page: pageParams.page + 1,
      last: pageData.last,
    });
  };

  const prev = () => {
    setPageParams({
      ...pageParams,
      page: pageParams.page - 1,
      last: pageData.last,
    });
  };

  const query = useLibraryData(scope, pageParams);
  const mutation = useSync(scope, pageParams);

  useEffect(() => {
    if (mutation.isSuccess) {
      const timeout = setTimeout(() => query.refetch(), 25 * 1000);

      return () => clearTimeout(timeout);
    }
  }, [mutation.isSuccess, query]);

  useEffect(() => {
    if (!query.data) {
      return;
    }

    const newPageData: LibraryParams = {
      total: query.data.total,
      page: query.data.page,
      page_size: query.data.page_size,
      last: undefined,
    };

    if (scope === LibraryKey.LibraryArtists) {
      const lastItem = last(query.data.data as LibraryArtist[])?.spotify_id;

      setPageData({
        ...newPageData,
        last: lastItem,
      });
    } else {
      setPageData(newPageData);
    }

    return () => {};
  }, [query.data, scope]);

  return (
    <div
      className={[
        "bg-gradient-to-b from-emerald-600 to-50% via-emerald-500 via-50%",
        "flex-1 flex flex-col justify-between gap-8",
        "pt-8",
        "overflow-y-auto",
        "divide-y-[0.5px]",
      ].join(" ")}
    >
      <div className="flex mx-32 px-8">
        <header className="flex-1">
          <h1 className="text-3xl font-bold text-zinc-100 tracking-tight font-headings">
            Dashboard
          </h1>
          <p className="text-zinc-100">
            View your stats and library at a glance.
          </p>
        </header>
      </div>
      <main
        className={["flex-1 flex flex-col justify-between gap-8", "p-8"].join(
          " "
        )}
      >
        {query.data ? (
          <Drawers
            scope={scope}
            ids={query.data.data.map((item) => item.spotify_id)}
          />
        ) : null}
        <section className="flex flex-col gap-4 flex-1 text-sm mx-32">
          <section className="flex w-full gap-4">
            {Counts.map((key) => (
              <StatCard key={key} scope={key} />
            ))}
          </section>
          <div className="flex-shrink">
            <Tabs scope={scope} onChange={onTabChange} context={mutation} />
          </div>
          <div className="flex flex-1 gap-8 pb-4">
            <div className={["flex-1 flex flex-col gap-4"].join(" ")}>
              <RealTimeTable
                scope={scope}
                context={query}
                pageData={pageData}
                pager={{ next, prev }}
              />
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
