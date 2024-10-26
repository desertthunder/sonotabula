import { formatDuration } from "@libs/helpers";
import { FetchError, Pagination, BrowserTrack } from "@libs/types";
import { useTokenStore } from "@/store";
import { useQuery } from "@tanstack/react-query";
import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table";
import React from "react";

const columnHelper = createColumnHelper<BrowserTrack>();

const columns = [
  columnHelper.display({
    header: "Album Art",
    id: "album_art",
    cell: (props) => (
      <img
        src={props.row.original.album_art}
        className="w-16"
        alt={`Album art for ${props.row.original.album_name}`}
      />
    ),
  }),
  columnHelper.accessor("name", {
    header: "Name",
    id: "name",
    meta: { className: "w-1/4 max-w-1/3" },
  }),
  columnHelper.accessor("album_name", {
    header: "Album",
    id: "album_name",
    meta: { className: "w-1/4 max-w-1/3" },
  }),
  columnHelper.accessor("duration", {
    header: "Duration",
    id: "duration",
    cell: (props) => (
      <span className="text-xs">
        {formatDuration(props.row.original.duration)}
      </span>
    ),
    meta: { className: "w-1/4" },
  }),
  columnHelper.accessor("is_synced", {
    header: "Synced",
    id: "is_synced",
    cell: (props) => (
      <span className="text-center">
        {props.row.original.is_synced ? (
          <i className="i-ri-check-fill text-bold text-2xl text-green-500"></i>
        ) : (
          <i className="i-ri-close-fill text-bold text-2xl text-red-500"></i>
        )}
      </span>
    ),
    meta: {
      className: "text-center",
    },
  }),
  columnHelper.accessor("is_analyzed", {
    header: "Analyzed",
    id: "is_analyzed",
    cell: (props) => (
      <span className="text-center">
        {props.row.original.is_analyzed ? (
          <i className="i-ri-check-fill text-bold text-2xl text-green-500"></i>
        ) : (
          <i className="i-ri-close-fill text-bold text-2xl text-red-500"></i>
        )}
      </span>
    ),
    meta: {
      className: "text-center",
    },
  }),
  columnHelper.display({
    header: "Open",
    id: "spotify_url",
    cell: (props) => (
      <a
        href={props.row.original.spotify_url}
        target="_blank"
        rel="noopener noreferrer"
        className="text-lg hover:text-green-500"
      >
        <i className="i-ri-external-link-fill" />
      </a>
    ),
  }),
];

function useTracks(page: number) {
  const token = useTokenStore((s) => s.token);
  const query = useQuery({
    queryKey: ["browser-tracks", page],
    queryFn: async () => {
      const url = new URL("/api/browser/tracks", window.location.origin);
      url.searchParams.append("page", page.toString());
      url.searchParams.append("page_size", "10");

      const response = await fetch(`/api/browser/tracks`, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        return Promise.reject({
          code: response.status,
          message: response.statusText,
        } as FetchError);
      }

      const data = await response.json();

      return data as { data: BrowserTrack[]; pagination: Pagination };
    },
  });

  return query;
}

export function TracksTable() {
  const query = useTracks(1);

  const table = useReactTable({
    columns,
    data: query.data?.data || [],
    getCoreRowModel: getCoreRowModel(),
  });

  return (
    <>
      <table className="h-[400px] text-sm w-full p-4 relative">
        <thead className="text-sm font-bold">
          {table.getHeaderGroups().map((headerGroup) => (
            <tr
              key={headerGroup.id}
              className="bg-slate-50 bg-opacity-100 z-20"
            >
              {headerGroup.headers.map((header) => (
                <th
                  key={header.id}
                  className={[
                    "h-10 text-left align-middle font-medium text-slate-800",
                    "sticky overflow-x-visible top-0 bg-slate-50 z-20",
                    header.id.includes("is_") ? "text-center" : "",
                  ].join(" ")}
                >
                  {header.isPlaceholder
                    ? null
                    : flexRender(
                        header.column.columnDef.header,
                        header.getContext()
                      )}
                  <hr className="mt-4" />
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody className="last:border-b-0">
          {query.isLoading ? <div>Loading...</div> : null}
          {query.isError ? (
            <div>Error: {query.error.message}</div>
          ) : (
            table.getRowModel().rows.map((row) => (
              <tr
                key={row.id}
                className={[
                  "z-10",
                  "border-b transition-colors",
                  "bg-white",
                  "hover:bg-slate-200",
                  "even:bg-slate-100",
                  "hover:last:text-green-500",
                ].join(" ")}
              >
                {row.getVisibleCells().map((cell) => (
                  <td
                    key={cell.id}
                    className={[
                      "p-2 align-middle",
                      "text-sm",
                      cell.column.columnDef.meta?.className || "",
                    ].join(" ")}
                  >
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </td>
                ))}
              </tr>
            ))
          )}
        </tbody>
      </table>
    </>
  );
}

export function TracksPage(props: { children?: React.ReactNode }) {
  return (
    <>
      {props.children}
      <TracksTable />
    </>
  );
}
