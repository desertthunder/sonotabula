import { DataTable } from "@/components/DataTable/DataTable";
import { ResourceKey } from "@/libs/types";
import { useBrowse } from "@/libs/hooks";
import { Outlet } from "react-router-dom";
import { Flex, Text, Heading, Box, ScrollArea } from "@radix-ui/themes";

export function BrowserPage() {
  const context = useBrowse<ResourceKey.LibraryPlaylists>(
    ResourceKey.LibraryPlaylists
  );

  if (context.isLoading) {
    return <div>Loading...</div>;
  }

  if (context.isError) {
    return <div>Error: {context.error.message}</div>;
  }

  return (
    <Flex flexGrow="1" gap="8" justify="between" className="p-8">
      <Flex direction="column" gap="4">
        <Heading>Browser Library Playlists</Heading>
        <Text>View synced library</Text>
        <Box flexGrow="1">
          <Outlet />
          <ScrollArea
            style={{
              maxHeight: "500px",
            }}
          >
            {context.data && context.data.length > 0 ? (
              <DataTable response={context.data} />
            ) : (
              "No data"
            )}
          </ScrollArea>
        </Box>
      </Flex>
    </Flex>
  );
}
