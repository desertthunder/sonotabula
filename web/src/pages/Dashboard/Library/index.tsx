import { Tabs } from "./Tabs";
import { ResourceKey } from "@/libs/types";
import { useCallback, useState } from "react";
import { LibraryTable } from "./Table";
import { useFetch } from "@/libs/hooks";

const defaultKey = ResourceKey.LibraryPlaylists;

export function Library() {
  const [scope, setScope] = useState<ResourceKey>(defaultKey);
  const context = useFetch<typeof scope>(scope, 10);

  const onTabChange = useCallback((key: ResourceKey) => {
    setScope(key);
  }, []);

  return (
    <>
      <div className="flex-shrink">
        <Tabs scope={scope} onChange={onTabChange} />
      </div>
      {context.isLoading ? <p>Loading...</p> : null}
      {context.isError ? <p>Error</p> : null}
      {/* @ts-expect-error need to fix */}
      {context.data ? <LibraryTable scope={scope} data={context.data} /> : null}
    </>
  );
}
