import { Tabs } from "./Tabs";
import { ResourceKey } from "@/libs/types";
import React, { useCallback } from "react";
import { LibraryTable } from "./LibraryTable";
import { Box } from "@radix-ui/themes";

const defaultKey = ResourceKey.LibraryPlaylists;

export function Library() {
  const [scope, setScope] = React.useState(defaultKey);

  const onTabChange = useCallback((key: ResourceKey) => {
    setScope(key);
  }, []);

  return (
    <>
      <Box flexShrink="1">
        <Tabs scope={scope} onChange={onTabChange} />
      </Box>
      <Box className="pt-4">
        <LibraryTable scope={scope} />
      </Box>
    </>
  );
}
