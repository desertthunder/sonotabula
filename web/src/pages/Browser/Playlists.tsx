import { decodeUnicode } from "@/libs/helpers";
import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table";
import React, { useEffect } from "react";
import { usePlaylists } from "./hooks/playlists";
import { useQueryClient } from "@tanstack/react-query";

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

export function PlaylistTable(props: {
  data: Playlist[];
  page: number;
  pageSize: number;
  setTotalPages: (totalPages: number) => void;
  sortBy?: string;
  filters?: string;
}) {
  const table = useReactTable({
    columns,
    data: props.data || [],
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
          {table.getRowModel().rows.map((row) => (
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
          ))}
        </tbody>
      </table>
    </>
  );
}

function FilterForm({
  pageSize,
  setPageSize,
  sortBy,
  setSortBy,
}: {
  pageSize: number;
  setPageSize: (pageSize: number) => void;
  sortBy: string | undefined;
  setSortBy: (sortBy: string | undefined) => void;
}) {
  return (
    <form className="hidden gap-4 bg-slate-500 py-16 px-4">
      <label>Items per page</label>
      <input
        type="number"
        value={pageSize}
        onChange={(e) => setPageSize(Number(e.target.value))}
      />
      <label>Sort By</label>
      <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
        <option value="">None</option>
        <option value="name">Name</option>
        <option value="is_analyzed">Analyzed</option>
      </select>
    </form>
  );
}

export const PagerButton = ({
  label,
  icon,
  disabled,
  onClick,
}: {
  label: string;
  icon?: string;
  disabled?: boolean;
  onClick: () => void;
}) => (
  <button
    className={[
      "flex gap-2 items-center",
      "border border-slate-300",
      "rounded-md",
      "p-1",
      "bg-slate-100",

      disabled
        ? "cursor-not-allowed bg-slate-200 text-slate-500"
        : "cursor-pointer hover:bg-slate-200",
    ].join(" ")}
    onClick={onClick}
    disabled={disabled}
  >
    {icon && icon.includes("left") ? (
      <i className={`i-${icon} text-lg`} />
    ) : null}
    <span className="text-xs">{label}</span>
    {icon && icon.includes("right") ? (
      <i className={`i-${icon} text-lg`} />
    ) : null}
  </button>
);

export function Pager({
  page,
  setPage,
  totalPages,
}: {
  page: number;
  setPage: (page: number) => void;
  totalPages?: number;
}) {
  return (
    <div className="flex gap-4 m-4">
      <PagerButton
        label="Prev"
        icon="ri-arrow-left-s-line"
        disabled={page === 1}
        onClick={() => setPage(Math.max(1, page - 1))}
      />
      <span className={["flex gap-2 items-center", "", "text-xs"].join(" ")}>
        Page {page}
        {totalPages ? ` of ${totalPages}` : null}
      </span>
      <PagerButton
        label="Next"
        icon="ri-arrow-right-s-line"
        disabled={totalPages ? page === totalPages : true}
        onClick={() => setPage(Math.min(totalPages ? totalPages : 1, page + 1))}
      />
    </div>
  );
}

export function PlaylistsPage(props: { children: React.ReactNode }) {
  const [page, setPage] = React.useState(1);
  const [totalPages, setTotalPages] = React.useState<number>();
  const [pageSize, setPageSize] = React.useState(10);
  const [sortBy, setSortBy] = React.useState<string | undefined>();
  const [filters] = React.useState<string | undefined>();

  const client = useQueryClient();
  const query = usePlaylists({ page, pageSize }, client);

  useEffect(() => {
    if (query.data?.pagination) {
      setTotalPages(query.data.pagination.num_pages);
    }
  }, [query.data?.pagination, props]);

  useEffect(() => {
    if (pageSize) {
      client.invalidateQueries({
        predicate: (query) => {
          return query.queryKey[0] === "browser-playlists";
        },
      });
    }

    if (page) {
      client.invalidateQueries({
        queryKey: ["browser-playlists", page - 1],
      });
    }
  }, [page, pageSize, client]);

  return (
    <>
      {props.children}
      <div className="rounded-lg bg-slate-50 p-8 drop-shadow-lg">
        <h2 className="text-lg font-bold">Playlists</h2>
        <FilterForm
          pageSize={pageSize}
          setPageSize={setPageSize}
          sortBy={sortBy}
          setSortBy={setSortBy}
        />
        <div className="overflow-y-auto flex-1 max-h-[450px]">
          {query.isLoading ? <div>Loading...</div> : null}
          {query.isFetching ? <div>Fetching...</div> : null}
          {query.isError ? (
            <div>Error: {query.error.message}</div>
          ) : (
            <PlaylistTable
              data={query.data?.data || []}
              page={page}
              pageSize={pageSize}
              setTotalPages={setTotalPages}
              sortBy={sortBy}
              filters={filters}
            />
          )}
        </div>
        <Pager page={page} setPage={setPage} totalPages={totalPages} />
      </div>
    </>
  );
}
