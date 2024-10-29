import { LibraryParams, LibraryResponse } from "@/libs/hooks/api/v1";
import { decodeUnicode } from "@libs/helpers";
import type {
  LibraryAlbum,
  LibraryArtist,
  LibraryPlaylist,
  LibraryResourceType,
  LibraryTrack,
} from "@libs/types";
import { LibraryKey } from "@libs/types";
import { UseQueryResult } from "@tanstack/react-query";
import {
  createColumnHelper,
  DisplayColumnDef,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table";
import { useMemo } from "react";
import { TableRow } from "./row";
import { ErrorCell, LoaderCell, PlaylistNameCell } from "./cells";
import _ from "lodash";
import { Pager } from "@/pages/Browser/components/forms/pagination";

const artistColumnHelper = createColumnHelper<LibraryArtist>();
const playlistColumnHelper = createColumnHelper<LibraryPlaylist>();
const albumColumnHelper = createColumnHelper<LibraryAlbum>();
const trackColumnHelper = createColumnHelper<LibraryTrack>();

const playlistColumns = [
  playlistColumnHelper.display({
    header: () => null,
    id: "image_url",
    cell: (props) => (
      <img src={props.row.original.image_url} alt="album" className="h-12" />
    ),
  }),
  playlistColumnHelper.accessor("name", {
    header: "Name",
    id: "name",
    cell: PlaylistNameCell,
  }),
  playlistColumnHelper.display({
    header: "Description",
    id: "description",
    cell: (props) => (
      <span className="text-xs text-slate-400">
        {props.row.original.description
          ? decodeUnicode(props.row.original.description)
          : "None"}
      </span>
    ),
  }),
  playlistColumnHelper.accessor("owner_id", {
    header: "Owner",
    id: "owner_id",
    cell: (props) => (
      <a
        href={`https://open.spotify.com/user/${props.row.original.owner_id}`}
        className="align-middle flex items-center gap-2 group "
      >
        {props.row.original.owner_id === "spotify" ? (
          <span className="group-hover:text-green-500">Spotify</span>
        ) : (
          <span className="group-hover:text-green-500">Creator Profile</span>
        )}
        <i className="i-ri-external-link-line group-hover:text-green-500"></i>
      </a>
    ),
  }),
  playlistColumnHelper.accessor("num_tracks", {
    header: "#",
    id: "num_tracks",
  }),
  playlistColumnHelper.accessor("is_synced", {
    header: "Synced",
    id: "is_synced",
    cell: (props) => (
      <span
        className={[
          "text-xs",
          props.row.original.is_synced ? "text-green-500" : "text-slate-400",
        ].join(" ")}
      >
        {props.row.original.is_synced ? (
          <i className="i-ri-check-line text-green-500" />
        ) : (
          <>
            <i className="i-ri-close-line text-red-400" />
          </>
        )}
      </span>
    ),
  }),
  playlistColumnHelper.display({
    header: "Link",
    id: "link",
    cell: (props) => (
      <a
        className="hover:text-green-500 text-lg"
        href={props.row.original.link}
        target="_blank"
        rel="noreferrer"
      >
        <i className="i-ri-external-link-line"></i>
      </a>
    ),
  }),
];

const albumColumns = [
  albumColumnHelper.display({
    header: () => null,
    id: "image_url",
    cell: (props) => (
      <img src={props.row.original.image_url} alt="album" className="h-12" />
    ),
  }),
  albumColumnHelper.display({
    header: "Name",
    id: "name",
  }),

  albumColumnHelper.display({
    header: "Artist",
    id: "artist_name",
  }),
  albumColumnHelper.display({
    header: "#",
    id: "total_tracks",
  }),
  albumColumnHelper.display({
    header: "Year",
    id: "release_date",
    cell: (props) => (
      <span>{props.row.original.release_date.split("-")[0]}</span>
    ),
  }),
];

const trackColumns = [
  trackColumnHelper.display({
    header: "Name",
    id: "name",
  }),
  trackColumnHelper.display({
    header: "Artist",
    id: "artist_name",
  }),
  trackColumnHelper.display({
    header: "Album",
    id: "album_name",
  }),
  trackColumnHelper.display({
    header: "Duration",
    id: "duration_ms",
  }),
  trackColumnHelper.display({
    header: "Link",
    id: "link",
    cell: (props) => (
      <a
        className="hover:text-green-500 text-lg"
        href={props.row.original.link}
        target="_blank"
        rel="noreferrer"
      >
        <i className="i-ri-external-link-line"></i>
      </a>
    ),
  }),
];

const artistColumns = [
  artistColumnHelper.display({
    header: () => null,
    id: "image_url",
    cell: (props) => (
      <img src={props.row.original.image_url} alt="album" className="h-12" />
    ),
  }),
  artistColumnHelper.display({
    header: "Name",
    id: "name",
  }),
  artistColumnHelper.display({
    header: "Genres",
    id: "genres",
    cell: (props) => (
      <span>
        {Array.isArray(props.row.original.genres)
          ? props.row.original.genres.join(", ")
          : props.row.original.genres}
      </span>
    ),
  }),
  artistColumnHelper.display({
    header: "Link",
    id: "link",
    cell: (props) => (
      <a
        className="hover:text-green-500 text-lg"
        href={props.row.original.link}
        target="_blank"
        rel="noreferrer"
      >
        <i className="i-ri-external-link-line"></i>
      </a>
    ),
  }),
];

interface Props<T extends LibraryKey> {
  scope: T;
  context: UseQueryResult<LibraryResponse<T>>;
  pageData: LibraryParams;
  pager: {
    next: () => void;
    prev: () => void;
  };
}

const getSearchPlaceholder = (scope: LibraryKey) => {
  switch (scope) {
    case LibraryKey.LibraryAlbums:
      return "Search albums";
    case LibraryKey.LibraryArtists:
      return "Search artists";
    case LibraryKey.LibraryPlaylists:
      return "Search playlists";
    case LibraryKey.LibraryTracks:
      return "Search tracks";
    default:
      return "Search";
  }
};

export function RealTimeTable<T extends LibraryKey>({
  scope,
  context,
  pageData,
  pager,
}: Props<T>) {
  const columns = useMemo(() => {
    switch (scope) {
      case LibraryKey.LibraryAlbums:
        return albumColumns;
      case LibraryKey.LibraryArtists:
        return artistColumns;
      case LibraryKey.LibraryPlaylists:
        return playlistColumns;
      case LibraryKey.LibraryTracks:
        return trackColumns;
      default:
        throw new Error("Invalid scope");
    }
  }, [scope]);

  const table = useReactTable({
    columns: columns as DisplayColumnDef<LibraryResourceType<T>>[],
    data: context.data?.data || [],
    getCoreRowModel: getCoreRowModel(),
  });

  const placeholder = getSearchPlaceholder(scope);

  return (
    <div className="rounded-lg bg-slate-50 p-6 drop-shadow-lg">
      <div className={["flex-1 flex flex-col gap-4 pb-4"].join(" ")}>
        <div aria-roledescription="search form controls" className="flex">
          <input
            type="search"
            className="p-2 rounded-md rounded-r-none border-[0.5px] border-slate-400 flex-1 text-white"
            placeholder={placeholder}
            disabled
          />
          <button
            className={[
              "px-4 py-2 rounded-l-none rounded-md gap-2 flex items-center",
              "bg-green-400 border-[0.5px] border-slate-400",
              "text-zinc-100",
            ].join(" ")}
            disabled
          >
            <i className="i-ri-search-line"></i>
            <span>Search</span>
          </button>
        </div>
      </div>
      <div className={["overflow-y-auto", "max-h-[500px]"].join(" ")}>
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
          <tbody className="last:border-b-0">
            {context.isLoading ? (
              <TableRow>
                {columns.map((_c, index) => (
                  <LoaderCell
                    key={index}
                    loader={index === _.toInteger(columns.length / 2)}
                  />
                ))}
              </TableRow>
            ) : null}
            {context.isError ? (
              <TableRow>
                {columns.map((_c, index) => (
                  <ErrorCell
                    key={index}
                    error={index === _.toInteger(columns.length / 2)}
                  />
                ))}
              </TableRow>
            ) : null}
            {context.data
              ? table.getRowModel().rows.map((row) => (
                  <TableRow key={row.id}>
                    {row.getVisibleCells().map((cell) => (
                      <td
                        key={cell.id}
                        className={[
                          "p-2 align-middle",
                          "text-xs",
                          cell.column.columnDef.meta?.className || "",
                        ].join(" ")}
                      >
                        {flexRender(
                          cell.column.columnDef.cell,
                          cell.getContext()
                        )}
                      </td>
                    ))}
                  </TableRow>
                ))
              : null}
          </tbody>
        </table>
      </div>
      <Pager
        page={pageData.page}
        setPage={pager.next}
        totalPages={Math.ceil(pageData.total / pageData.page_size) + 1}
      />
    </div>
  );
}
