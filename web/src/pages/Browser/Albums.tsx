/**
 * @todo use react table
 * */

import { ResourceKey } from "@/libs/types";
import { Outlet } from "react-router-dom";
import { usePaginatedBrowser } from "@/libs/hooks/api/query";
import { useBrowserContext } from "./context";
import React from "react";

export function BrowseAlbumsPage() {
  const { setTitle, setDescription } = useBrowserContext();
  const query = usePaginatedBrowser<ResourceKey.BrowserAlbums>(
    ResourceKey.BrowserAlbums,
    { page: 1, page_size: 25 }
  );

  React.useEffect(() => {
    setTitle("Albums");
    setDescription("View synced albums");
  }, [setTitle, setDescription]);

  if (query.isLoading) {
    return <div>Loading...</div>;
  }

  if (query.isError) {
    return <div>Error: {query.error.message}</div>;
  }

  const data = query.data?.data;

  return (
    <>
      <Outlet />

      <table className="h-[400px] w-full table table-auto">
        <thead className="text-sm font-bold">
          <tr className="border-b-2 text-left">
            <th className="p-3">
              <span className="sr-only">Cover</span>
            </th>
            <th className="p-4 pl-0 pt-0">Album</th>
            <th className="p-4 pl-0 pt-0">Artist</th>
            <th className="p-4 pl-0 pt-0">Released</th>
            <th className="p-4 pl-0 pt-0">Link</th>
          </tr>
        </thead>
        <tbody className="text-xs font-medium">
          {data?.length && data.length > 0
            ? data.map((album) => (
                <tr
                  key={album.id}
                  className="border-b last:border-b-0 odd:bg-slate-100 hover:bg-slate-200"
                >
                  <td>
                    {album.image_url ? (
                      <img
                        src={album.image_url}
                        alt={album.name}
                        className="w-24"
                      />
                    ) : null}
                  </td>
                  <td className="w-1/4">{album.name}</td>
                  <td className="w-1/4">
                    {album.artists.map((artist) => artist.name).join(", ")}
                  </td>
                  <td>{album.release_year}</td>
                  <td>
                    <a
                      href={`https://open.spotify.com/album/${album.id}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="hover:text-green-500 hover:font-bold transition-colors text-lg"
                    >
                      <i className="i-ri-external-link-fill" />
                    </a>
                  </td>
                </tr>
              ))
            : "No data"}
        </tbody>
      </table>
    </>
  );
}
