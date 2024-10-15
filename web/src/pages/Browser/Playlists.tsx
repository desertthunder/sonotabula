import { decodeUnicode } from "@/libs/helpers";
import { FetchError } from "@/libs/types";
import { useTokenStore } from "@/store";
import { useQuery } from "@tanstack/react-query";
import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table";
import { Outlet } from "react-router-dom";
import { useBrowserContext } from "./context";
import React from "react";

type Playlist = {
  id: string;
  spotify_id: string;
  name: string;
  is_synced: boolean;
  is_analyzed: boolean;
  description?: string;
  owner_id?: string;
  version?: string;
  image_url?: string;
  public?: boolean;
  shared?: boolean;
};

type Pagination = {
  total: number;
  per_page: number;
  page: number;
};

const columnHelper = createColumnHelper<Playlist>();

const columns = [
  columnHelper.display({
    header: "Cover",
    id: "image_url",
    cell: (props) => (
      <img
        src={props.row.original.image_url}
        className="w-16"
        alt={`Cover for ${props.row.original.spotify_id}`}
      />
    ),
  }),
  columnHelper.accessor("name", {
    header: "Name",
    id: "name",
    meta: { className: "w-1/4 max-w-1/3" },
  }),
  columnHelper.accessor("description", {
    header: "Description",
    id: "description",
    cell: (props) => (
      <span className="text-xs">
        {props.row.original.description ? (
          decodeUnicode(props.row.original.description)
        ) : (
          <em className="text-gray-400">None set</em>
        )}
      </span>
    ),
    meta: {
      className: "w-1/3 max-w-1/2",
    },
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
    header: "Link",
    id: "spotify_id",
    cell: (props) => (
      <a
        href={`https://open.spotify.com/playlist/${props.row.original.spotify_id}`}
        target="_blank"
        rel="noreferrer"
        className="hover:text-green-500 text-lg"
      >
        <i className="i-ri-external-link-fill" />
      </a>
    ),
  }),
];

function usePlaylists() {
  const token = useTokenStore((s) => s.token);
  const query = useQuery({
    queryKey: ["browser-playlists"],
    queryFn: async () => {
      const response = await fetch(`/api/browser/playlists`, {
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
      console.log(data);
      return data as { data: Playlist[]; pagination: Pagination };
    },
  });

  return query;
}

export function PlaylistTable() {
  const query = usePlaylists();

  const table = useReactTable({
    columns,
    data: query.data?.data || [],
    getCoreRowModel: getCoreRowModel(),
  });

  const { setPagination } = useBrowserContext();

  React.useEffect(() => {
    if (query.data?.pagination && query.data?.data) {
      setPagination({
        ...query.data.pagination,
        count: query.data.data.length,
      });
    }
  }, [query.data?.data, query.data?.pagination, setPagination]);

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

export function PlaylistsPage() {
  const { setTitle, setDescription } = useBrowserContext();

  React.useEffect(() => {
    setTitle("Playlists");
    setDescription("View synced playlists");
  }, [setTitle, setDescription]);

  return (
    <>
      <Outlet />
      <PlaylistTable />
    </>
  );
}
