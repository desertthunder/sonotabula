import { DataTable } from "@/components/DataTable/DataTable";
import { ResourceKey } from "@/libs/types";
import { useBrowse } from "@/libs/hooks";
import { Outlet } from "react-router-dom";

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
    <div className="flex flex-1 gap-8 p-8 justify-between text-sm">
      <section className="flex flex-col gap-4 flex-1">
        <h1 className="font-medium text-base">Browser Library Playlists</h1>
        <h2>View synced library</h2>
        <div className="flex-1">
          <Outlet />
          {context.data && context.data.length > 0 ? (
            <DataTable response={context.data} />
          ) : (
            "No data"
          )}
        </div>
      </section>
    </div>
  );
}

export { BrowserLayout } from "./Layout";
