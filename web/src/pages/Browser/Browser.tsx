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
    <div className="flex flex-col">
      <section className="p-6 pb-0 space-y-2">
        <h1 className="font-headings text-gray-50 text-[1.5rem] font-medium">
          Data Browser
        </h1>
        <h3 className="font-headings text-gray-200">View synced library</h3>
        <Outlet />
      </section>
      <section className="p-8 flex-1 space-x-4 grid grid-rows-12 max-h-[620px]">
        <div className="card col-span-12 p-4 row-span-12">
          <h2 className="font-headings text-gray-800 pb-4 border-b mb-4 border-b-black text-[1.25rem] font-medium">
            Library Playlists
          </h2>
          <div className="p-0 m-0 max-h-full w-full overflow-y-auto ">
            {context.data && context.data.length > 0 ? (
              <DataTable response={context.data} />
            ) : (
              "No data"
            )}
          </div>
        </div>
      </section>
    </div>
  );
}
