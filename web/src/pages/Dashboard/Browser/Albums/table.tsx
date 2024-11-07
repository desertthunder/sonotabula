import type { BrowserAlbum, BrowserAlbumListResponse } from "@/libs/types/api";
import { UseQueryResult } from "@tanstack/react-query";
import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table";
import _ from "lodash";
import { Link } from "wouter";

const columnHelper = createColumnHelper<BrowserAlbum>();
const columns = [
  columnHelper.accessor("image_url", {
    header: () => null,
    cell: (props) => (
      <p className="flex items-center max-w-fit">
        <img src={props.getValue()} className="w-24" alt="Album Image" />
      </p>
    ),
  }),
  columnHelper.accessor("id", {
    header: "Name",
    cell: (props) => {
      return (
        <Link
          to={`/dashboard/browser/albums/${props.getValue()}`}
          className={[
            "hover:text-primary hover:underline hover:font-semibold hover:text-base",
            "transition-all duration-300 ease-in-out",
            "pointer-events-none",
          ].join(" ")}
        >
          {props.row.original.name}
        </Link>
      );
    },
  }),

  columnHelper.accessor("artists", {
    id: "artist_names",
    header: "Artists",
    cell: (props) => (
      <p>
        {props
          .getValue()
          .map((artist) => artist.name)
          .join(", ")}
      </p>
    ),
  }),
  columnHelper.accessor("release_year", {
    header: "Release Year",
    cell: (props) => {
      return <p>{props.getValue()}</p>;
    },
  }),
  columnHelper.accessor("tracks", {
    id: "number_of_tracks",
    header: "Total Tracks",
    cell: (props) => {
      return <p>{props.getValue().length}</p>;
    },
  }),
  columnHelper.accessor("tracks", {
    id: "track_names",
    header: "Tracks",
    cell: (props) => (
      <p className="grid grid-cols-3 gap-2 max-w-fit">
        {_.take(props.getValue(), 12).map((track) => (
          <span
            key={track.spotify_id}
            className="truncate w-32 max-w-full"
            title={track.name}
          >
            {track.name}
          </span>
        ))}
        {props.getValue().length > 12 ? (
          <span className="text-gray-500">...</span>
        ) : null}
      </p>
    ),
  }),
];

export function Table({
  context,
}: {
  context: UseQueryResult<BrowserAlbumListResponse, Error>;
}) {
  const table = useReactTable({
    columns,
    data: context.data?.data || [],
    getCoreRowModel: getCoreRowModel(),
  });

  return (
    <section className="overflow-auto">
      <table className="w-full rounded-box text-left text-sm">
        <thead className="font-sans text-base text-left bg-primary text-surface">
          {table.getHeaderGroups().map((headerGroup) => (
            <tr key={headerGroup.id}>
              {headerGroup.headers.map((header) => (
                <th
                  key={header.id}
                  className={["px-4 py-3 align-middle", "font-semibold"].join(
                    " "
                  )}
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
          {context.isLoading ? (
            <tr className="bg-surface even:bg-green-200">
              <td
                colSpan={columns.length}
                className="text-center text-3xl p-12"
              >
                <i className="i-ri-loader-line animate-spin" />
              </td>
            </tr>
          ) : context.isError ? (
            <tr className="bg-surface even:bg-green-200 text-red-500">
              <td colSpan={columns.length} className="px-4">
                Unable to fetch albumss: {context.error.message}
              </td>
            </tr>
          ) : (
            table.getRowModel().rows.map((row) => (
              <tr
                key={row.id}
                className={[
                  "bg-surface hover:bg-green-200 text-sm border-y border-green-200",
                  "hover:bg-green-200",
                ].join(" ")}
              >
                {row.getVisibleCells().map((cell) => (
                  <td
                    key={cell.id}
                    className={[
                      "px-4 py-3 align-middle whitespace-normal",
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
