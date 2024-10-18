import { useFetch } from "@/libs/hooks";
import { ResourceKey } from "@/libs/types";
import { Counts } from "@/libs/types/api";
import { useCallback, useState } from "react";
import { StatCard } from "./components/stats";
import { LibraryTable } from "./components/tables";
import { Tabs } from "./components/tabs";

export function Dashboard() {
  const [scope, setScope] = useState<ResourceKey>(ResourceKey.LibraryPlaylists);
  const context = useFetch<typeof scope>(scope, 10);

  const onTabChange = useCallback((key: ResourceKey) => {
    setScope(key);
  }, []);

  return (
    <main
      className={[
        "bg-gradient-to-b from-emerald-600 to-50% via-emerald-500 via-50%",
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
          <div className="flex-shrink gap-x-2 flex items-center justify-between">
            <button className="bg-white text-emerald-600 rounded-lg p-2">
              <i className="i-ri-user-3-line" />
              Profile
            </button>
            <button className="bg-white text-emerald-600 rounded-lg p-2">
              <i className="i-ri-refresh-line" />
              Refresh
            </button>
            <button className="bg-white text-emerald-600 rounded-lg p-2">
              <i className="i-ri-settings-3-line" />
              Settings
            </button>
            <button className="text-4xl text-white">
              <i className="i-ri-thunderstorms-line" />
            </button>
          </div>
        </div>

        <div className="flex-shrink">
          <Tabs scope={scope} onChange={onTabChange} />
        </div>
        <div className="flex flex-1 gap-8">
          <div className="flex-1 flex flex-col gap-4">
            {context.isLoading ? <p>Loading...</p> : null}
            {context.isError ? <p>Error</p> : null}
            {context.data ? (
              //@ts-expect-error need to fix
              <LibraryTable scope={scope} data={context.data} />
            ) : null}
          </div>
          <section className="flex flex-col gap-4 min-w-[25%]">
            {Counts.map((key) => (
              <StatCard key={key} scope={key} />
            ))}
          </section>
        </div>
      </section>
    </main>
  );
}
