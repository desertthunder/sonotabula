/**
 * @description index of /dashboard url namespace
 */
import { LibraryKey, Counts } from "@libs/types";
import { useCallback, useEffect, useState } from "react";
import { StatCard } from "./components/stats";
import { Tabs } from "./components/tabs";
import { Drawers } from "./components/drawers";
import { RealTimeTable } from "./components/tables";
import type { DrawerKey } from "@/store/drawers";
import { LibraryParams, useLibraryData, useSync } from "@/libs/hooks/api/v1";

const initialParams = {
  total: 0,
  page: 1,
  page_size: 10,
};

export function Dashboard() {
  const [scope, setScope] = useState<LibraryKey>(LibraryKey.LibraryPlaylists);
  const [pageParams, setPageParams] = useState<LibraryParams>(initialParams);
  const [pageData, setPageData] = useState<LibraryParams>(initialParams);

  const onTabChange = useCallback((key: LibraryKey) => {
    setScope(key);
    setPageParams(initialParams);
  }, []);

  const next = () => {
    setPageParams({
      ...pageParams,
      page: pageParams.page + 1,
    });
  };

  const prev = () => {
    setPageParams({
      ...pageParams,
      page: pageParams.page - 1,
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

    setPageData({
      total: query.data.total,
      page: query.data.page,
      page_size: query.data.page_size,
    });
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
            r={{
              [LibraryKey.LibraryPlaylists]: query.data.data.map(
                (p) =>
                  `${LibraryKey.LibraryPlaylists}-${p.spotify_id}` as DrawerKey
              ),
            }}
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
