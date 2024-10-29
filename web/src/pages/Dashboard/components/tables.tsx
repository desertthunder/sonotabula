import { LibraryParams, LibraryResponse } from "@/libs/hooks/api/v1";
import { decodeUnicode, formatDuration } from "@libs/helpers";
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
import {
  ErrorCell,
  LoaderCell,
  PlaylistIsSyncedCell,
  PlaylistNameCell,
  TrackIsAnalyzedCell,
  TrackIsSyncedCell,
  TrackNameCell,
} from "./cells";
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
    cell: PlaylistIsSyncedCell,
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
  albumColumnHelper.accessor("image_url", {
    header: () => null,
    id: "image_url",
    cell: (props) => (
      <img src={props.getValue()} alt="album" className="h-12" />
    ),
  }),
  albumColumnHelper.accessor("name", {
    header: "Name",
    id: "name",
  }),

  albumColumnHelper.accessor("artist_name", {
    header: "Artist",
    id: "artist_name",
  }),
  albumColumnHelper.accessor("total_tracks", {
    header: "#",
    id: "total_tracks",
  }),
  albumColumnHelper.accessor("release_date", {
    header: "Year",
    id: "release_date",
    cell: (props) => <span>{props.getValue().split("-")[0]}</span>,
  }),
  albumColumnHelper.accessor("spotify_id", {
    header: "Link",
    id: "spotify_id",
    cell: (props) => (
      <a
        href={`https://open.spotify.com/album/${props.getValue()}`}
        target="_blank"
        rel="noreferrer"
        className="hover:text-green-500 flex items-center gap-2"
      >
        <span>Open</span>
        <i className="i-ri-external-link-line"></i>
      </a>
    ),
  }),
];

const trackColumns = [
  trackColumnHelper.accessor("image_url", {
    header: () => null,
    id: "image_url",
    cell: (props) => (
      <img src={props.row.original.image_url} alt="album" className="h-12" />
    ),
  }),
  trackColumnHelper.accessor("name", {
    header: "Name",
    id: "name",
    cell: TrackNameCell,
  }),
  trackColumnHelper.accessor("artist_name", {
    header: "Artist",
    id: "artist_name",
  }),
  trackColumnHelper.accessor("album_name", {
    header: "Album",
    id: "album_name",
  }),
  trackColumnHelper.accessor("duration_ms", {
    header: "Duration",
    id: "duration_ms",
    cell: (props) => <span>{formatDuration(props.getValue())}</span>,
  }),
  trackColumnHelper.accessor("is_synced", {
    header: "Synced",
    id: "is_synced",
    cell: TrackIsSyncedCell,
  }),
  trackColumnHelper.accessor("is_analyzed", {
    header: "Analyzed",
    id: "is_analyzed",
    cell: TrackIsAnalyzedCell,
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
  artistColumnHelper.accessor("image_url", {
    header: () => null,
    id: "image_url",
    cell: (props) => (
      <img src={props.getValue()} alt="album" className="h-12" />
    ),
  }),
  artistColumnHelper.accessor("name", {
    header: "Name",
    id: "name",
  }),
  artistColumnHelper.accessor("genres", {
    header: "Genres",
    id: "genres",
    cell: (props) => (
      <span>
        {Array.isArray(props.getValue())
          ? props.getValue().join(", ")
          : props.getValue()}
      </span>
    ),
  }),
  artistColumnHelper.accessor("spotify_id", {
    header: "Link",
    id: "spotify_id",
    cell: (props) => (
      <a
        href={`https://open.spotify.com/artist/${props.getValue()}`}
        target="_blank"
        rel="noreferrer"
        className="hover:text-green-500 flex items-center gap-2"
      >
        <span>Open</span>
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

  return (
    <div className="rounded-lg bg-slate-50 p-6 drop-shadow-lg">
      <div className={["overflow-y-auto", "max-h-[450px]"].join(" ")}>
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
                      "h-10 text-left align-middle font-medium text-gray-500 text-xs",
                      "sticky overflow-x-visible top-0 bg-slate-50 z-20 uppercase",
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
