import { Tabs } from "./Tabs";
import { ResourceKey } from "@/libs/types";
import { useCallback, useState } from "react";
import { LibraryTable } from "./Table";
import { Box } from "@radix-ui/themes";
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
      <Box flexShrink="1">
        <Tabs scope={scope} onChange={onTabChange} />
      </Box>
      <Box className="pt-4">
        {context.isLoading ? <p>Loading...</p> : null}
        {context.isError ? <p>Error</p> : null}
        {context.data ? (
          <LibraryTable scope={scope} data={context.data} />
        ) : null}
      </Box>
    </>
  );
}
