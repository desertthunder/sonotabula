import { Tabs } from "./Tabs";
import { ResourceKey } from "@/libs/types";
import React, { useCallback } from "react";
import { LibraryTable } from "./LibraryTable";

const defaultKey = ResourceKey.LibraryPlaylists;

export function LibraryCard() {
  const [scope, setScope] = React.useState(defaultKey);

  const onTabChange = useCallback((key: ResourceKey) => {
    setScope(key);
  }, []);

  return (
    <div className="card library h-full">
      <header>
        <h1 className="text-xl font-bold leading-none text-gray-900 sm:text-2xl">
          Library
        </h1>
        <h2 className="">I dunno</h2>
      </header>
      <Tabs scope={scope} onChange={onTabChange} />
      <main>
        <LibraryTable scope={scope} />
      </main>
    </div>
  );
}
