import { LibraryKey, Counts } from "@libs/types";
import { useCallback, useEffect, useState } from "react";
import { StatCard } from "./components/stats";
import { Tabs } from "./components/tabs";
import { RealTimeTable } from "./components/tables";
import {
  LibraryParams,
  useLibraryPlaylists,
  useSyncPlaylists,
} from "@/libs/hooks/api/v1";

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

  const query = useLibraryPlaylists(scope, pageParams);
  const mutation = useSyncPlaylists(scope, pageParams);

  useEffect(() => {
    if (mutation.isSuccess) {
      query.refetch();
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
  }, [query.data]);

  return (
    <main
      className={[
        "bg-gradient-to-b from-emerald-600 to-70% via-emerald-500 via-70%",
        "flex-1 flex justify-between gap-8",
        "px-8 pt-4",
        "overflow-y-auto",
      ].join(" ")}
    >
      <section className="flex flex-col gap-4 flex-1 text-sm">
        <div className="flex">
          <header className="flex-1">
            <h1 className="text-2xl font-semibold text-zinc-100">Dashboard</h1>
            <p className="text-zinc-100">
              View your stats and library at a glance.
            </p>
          </header>
        </div>

        <div className="flex-shrink">
          <Tabs scope={scope} onChange={onTabChange} context={mutation} />
        </div>
        <div className="flex flex-1 gap-8 pb-4">
          <div className={["flex-1 flex flex-col gap-4"].join(" ")}>
            <RealTimeTable
              scope={scope}
              context={query}
              handler={() => console.debug("Row clicked")}
              pageData={pageData}
              pager={{ next, prev }}
            />
          </div>
        </div>
      </section>
      <section className="flex flex-col max-h-fit gap-4 min-w-[25%]">
        {Counts.map((key) => (
          <StatCard key={key} scope={key} />
        ))}
      </section>
    </main>
  );
}
