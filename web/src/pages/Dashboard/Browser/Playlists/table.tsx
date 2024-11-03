import { useTokenStore } from "@/store";
import { useQuery } from "@tanstack/react-query";
import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table";
import _ from "lodash";
import { useEffect, useMemo } from "react";
import { usePlaylistFilters } from "@/store/filters";
import type { BrowserPlaylist } from "./types";
import { PlaylistActionsCell } from "./cells";
import { Link } from "wouter";

const columnHelper = createColumnHelper<BrowserPlaylist>();

const columns = [
  columnHelper.accessor("image_url", {
    header: () => null,
    cell: (props) => (
      <p className="min-w-8">
        <img src={props.getValue()} className="w-16" alt="Playlist Image" />
      </p>
    ),
  }),
  columnHelper.accessor("name", {
    header: "Name",
    cell: (props) => {
      const id = props.row.original.id;
      return (
        <Link
          to={`/dashboard/browser/playlists/${id}`}
          className={[
            "hover:text-primary hover:underline hover:font-semibold hover:text-base",
            "transition-all duration-300 ease-in-out",
          ].join(" ")}
        >
          {props.getValue()}
        </Link>
      );
    },
  }),
  columnHelper.accessor("description", {
    header: () => (
      <>
        <span className="hidden lg:inline">Description</span>
        <span className="lg:hidden">Desc.</span>
      </>
    ),
    cell: (props) => (
      <p className="max-w-64 truncate">
        {props.getValue() ? (
          props.getValue()
        ) : (
          <span className="text-gray-500 italic">None</span>
        )}
      </p>
    ),
  }),
  columnHelper.accessor("owner_id", {
    header: "Owner",
  }),
  columnHelper.accessor("public", {
    header: "Public",
    cell: (props) => {
      return (
        <span className={props.getValue() ? "text-green-500" : "text-red-500"}>
          {props.getValue() ? "Yes" : "No"}
        </span>
      );
    },
  }),
  columnHelper.accessor("shared", {
    header: "Shared",
    cell: (props) => {
      return (
        <span className={props.getValue() ? "text-green-500" : "text-red-500"}>
          {props.getValue() ? "Yes" : "No"}
        </span>
      );
    },
  }),
  columnHelper.accessor("is_analyzed", {
    header: () => {
      return (
        <>
          <span className="hidden lg:inline">Analyzed</span>
          <i className="lg:hidden i-ri-line-chart-line" />
        </>
      );
    },
    cell: (props) =>
      props.getValue() ? (
        <i className="i-ri-check-line text-primary" />
      ) : (
        <i className="i-ri-close-line text-error" />
      ),
  }),
  columnHelper.accessor("id", {
    header: "Actions",
    cell: (props) => <PlaylistActionsCell playlistID={props.getValue()} />,
  }),
  columnHelper.accessor("spotify_id", {
    header: "Link",
    cell: (props) => {
      const link = `https://open.spotify.com/playlist/${props.getValue()}`;
      return (
        <a href={link} target="_blank" rel="noreferrer">
          Open
        </a>
      );
    },
  }),
];

async function fetchPlaylists(token: string | null, params: URLSearchParams) {
  const uri = new URL(
    "/server/api/v1/browser/playlists",
    window.location.origin
  );
  uri.search = params.toString();
  const response = await fetch(uri.toString(), {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch playlists");
  }

  return (await response.json()) as {
    data: BrowserPlaylist[];
    pagination: {
      total: number;
      per_page: number;
      page: number;
      num_pages: number;
    };
  };
}

export function Table() {
  const token = useTokenStore((state) => state.token);
  const updateTotal = usePlaylistFilters((state) => state.updateTotal);
  const page = usePlaylistFilters((state) => state.page);
  const pageSize = usePlaylistFilters((state) => state.pageSize);
  const updateFetching = usePlaylistFilters((state) => state.updateFetching);
  const filters = usePlaylistFilters((state) => state.filters);

  const params = useMemo(() => {
    const params = new URLSearchParams();
    params.set("page", page.toString());
    params.set("page_size", pageSize.toString());

    for (const [key, value] of filters) {
      params.set(key, value);
    }

    return params;
  }, [page, pageSize, filters]);

  const query = useQuery({
    queryKey: _.flatten([
      "browser",
      "playlists",
      ...Array.from(params.entries()),
    ]),
    queryFn: async () => {
      const data = await fetchPlaylists(token, params);

      return data;
    },
  });

  const table = useReactTable({
    columns,
    data: query.data?.data || [],
    getCoreRowModel: getCoreRowModel(),
  });

  useEffect(() => {
    if (query.data) {
      updateTotal(query.data.pagination.total);
    }
  }, [query.data, updateTotal]);

  useEffect(() => {
    const isFetching = query.isLoading || query.isFetching || query.isFetching;

    updateFetching(isFetching);
  }, [query.isLoading, query.isFetching, updateFetching]);

  return (
    <section className="overflow-auto">
      <table className="table-fixed lg:table-auto w-full border-collapse">
        <thead className="font-sans text-base text-left bg-primary text-surface">
          {table.getHeaderGroups().map((headerGroup) => (
            <tr key={headerGroup.id}>
              {headerGroup.headers.map((header) => (
                <th
                  key={header.id}
                  className={[
                    "p-2",
                    "font-semibold",
                    "border-r border-slate-200 last:border-none",
                  ].join(" ")}
                >
                  {header.isPlaceholder
                    ? null
                    : flexRender(
                        header.column.columnDef.header,
                        header.getContext()
                      )}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody>
          {query.isLoading ? (
            <tr className="bg-surface even:bg-green-200 text-xs">
              <td
                colSpan={columns.length}
                className="text-center text-3xl p-12"
              >
                <i className="i-ri-loader-line animate-spin" />
              </td>
            </tr>
          ) : query.isError ? (
            <tr className="bg-surface even:bg-green-200 text-xs text-red-500">
              <td colSpan={columns.length} className="px-4">
                Unable to fetch playlists: {query.error.message}
              </td>
            </tr>
          ) : (
            table.getRowModel().rows.map((row) => (
              <tr key={row.id} className="bg-surface even:bg-green-200 text-xs">
                {row.getVisibleCells().map((cell) => (
                  <td
                    key={cell.id}
                    className={[
                      "border-r border-slate-300 last:border-none px-2",
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
    </section>
  );
}
