import { decodeUnicode } from "@/libs/helpers";
import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table";
import { useState } from "react";
import {
  useFocus,
  useDismiss,
  useRole,
  useInteractions,
  autoUpdate,
  offset,
  flip,
  shift,
  useFloating,
  useClick,
} from "@floating-ui/react";

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
    header: () => null,
    id: "id",
    cell: (props) => (
      <form>
        <input
          type="checkbox"
          id={props.row.original.id}
          name={props.row.original.id}
          value={props.row.original.id}
        />
      </form>
    ),
  }),
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
  columnHelper.display({
    header: "Actions",
    cell: function Cell(_props) {
      const [isOpen, setIsOpen] = useState(false);

      const { refs, floatingStyles, context } = useFloating({
        open: isOpen,
        onOpenChange: setIsOpen,
        middleware: [
          offset(10),
          flip({
            mainAxis: false,
          }),
          shift(),
        ],
        whileElementsMounted: autoUpdate,
      });

      const click = useClick(context);
      const focus = useFocus(context);
      const dismiss = useDismiss(context);
      const role = useRole(context, {
        // If your reference element has its own label (text).
        role: "tooltip",
        // If your reference element does not have its own label,
        // e.g. an icon.
        // role: "label",
      });

      // Merge all the interactions into prop getters
      const { getReferenceProps, getFloatingProps } = useInteractions([
        focus,
        dismiss,
        role,
        click,
      ]);
      return (
        // ReSync, View, Analyze, Delete/Unfollow
        <div className="flex flex-col text-xs relative">
          <button
            className="px-2 py-1 text-zinc-600 group"
            ref={refs.setReference}
            {...getReferenceProps()}
          >
            <i className="i-ri-more-fill text-lg group-hover:text-black group-hover:scale-125 transition-transform duration-500" />
          </button>
          {isOpen ? (
            <div
              ref={refs.setFloating}
              style={floatingStyles}
              {...getFloatingProps()}
              className="flex gap-1 ring-2 ring-zinc-100 shadow-xl drop-shadow-2xl w-fit bg-zinc-100 p-2 rounded-md z-[100]"
            >
              <button className="hover:bg-primary p-1 rounded-md">
                <i className="i-ri-refresh-line text-lg" />
              </button>
              <button className="hover:bg-secondary p-1 rounded-md">
                <i className="i-ri-eye-fill text-lg" />
              </button>
              <button className="hover:bg-green-400 p-1 rounded-md">
                <i className="i-ri-bar-chart-fill text-lg" />
              </button>
              <button className="hover:bg-red-400 p-1 rounded-md">
                <i className="i-ri-delete-bin-6-fill text-lg" />
              </button>
            </div>
          ) : null}
        </div>
      );
    },
  }),
];

export function PlaylistTable(props: {
  data: Playlist[];
  page: number;
  pageSize: number;
  setTotalPages: (totalPages: number) => void;
  sortBy?: string;
  filters?: string[][];
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
              key={
                headerGroup.id +
                headerGroup.headers.map((h) => h.colSpan).join("")
              }
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
