import { DrawerKey, useDrawerStore } from "@/store/drawers";
import type {
  LibraryAlbum,
  LibraryArtist,
  LibraryPlaylist,
  LibraryTrack,
} from "@libs/types";
import { LibraryKey } from "@libs/types";
import type { CellContext } from "@tanstack/react-table";
import { useCallback } from "react";

export function PlaylistNameCell(props: CellContext<LibraryPlaylist, string>) {
  const id = props.row.original.spotify_id;
  const drawerKey: DrawerKey = `${LibraryKey.LibraryPlaylists}-${id}`;
  const toggleDrawer = useDrawerStore((state) => state.toggleDrawer);

  const toggleFn = useCallback(() => {
    toggleDrawer(drawerKey);
  }, [toggleDrawer, drawerKey]);

  return (
    <button
      onClick={toggleFn}
      className="text-left text-xs text-slate-800 hover:text-primary"
    >
      {props.getValue()}
    </button>
  );
}

export function TrackNameCell(props: CellContext<LibraryTrack, string>) {
  const id = props.row.original.spotify_id;
  const drawerKey: DrawerKey = `${LibraryKey.LibraryTracks}-${id}`;
  const toggleDrawer = useDrawerStore((state) => state.toggleDrawer);

  const toggleFn = useCallback(() => {
    toggleDrawer(drawerKey);
  }, [toggleDrawer, drawerKey]);

  return (
    <button
      onClick={toggleFn}
      className="text-left text-xs text-slate-800 hover:text-primary"
    >
      {props.getValue()}
    </button>
  );
}

interface LoaderCellProps {
  loader: boolean;
}

export function LoaderCell(props: LoaderCellProps) {
  if (props.loader) {
    return (
      <td className="p-2 align-middle text-xs text-slate-400">
        <span>Loading...</span>
        <i className="i-ri-loader-5-fill animate-spin"></i>
      </td>
    );
  } else {
    return <td className="p-2 align-middle text-xs text-slate-400" />;
  }
}

interface ErrorCellProps {
  error: boolean;
}

export function ErrorCell(props: ErrorCellProps) {
  if (props.error) {
    return (
      <td className="p-2 align-middle text-xs text-slate-400">
        <span className="text-red-500">Error</span>
        <i className="i-ri-error-warning-fill"></i>
      </td>
    );
  } else {
    return <td className="p-2 align-middle text-xs text-slate-400" />;
  }
}

export function PlaylistIsSyncedCell(
  props: CellContext<LibraryPlaylist, boolean>
) {
  return (
    <span className={["text-xs"].join(" ")}>
      {props.getValue() ? (
        <i className="i-ri-check-line text-green-500" />
      ) : (
        <>
          <i className="i-ri-close-line text-red-400" />
        </>
      )}
    </span>
  );
}

export function TrackIsSyncedCell(props: CellContext<LibraryTrack, boolean>) {
  return (
    <span className={["text-xs"].join(" ")}>
      {props.getValue() ? (
        <i className="i-ri-check-line text-green-500" />
      ) : (
        <>
          <i className="i-ri-close-line text-red-400" />
        </>
      )}
    </span>
  );
}

export function ArtistIsSyncedCell(props: CellContext<LibraryArtist, boolean>) {
  return (
    <span className={["text-xs"].join(" ")}>
      {props.getValue() ? (
        <i className="i-ri-check-line text-green-500" />
      ) : (
        <>
          <i className="i-ri-close-line text-red-400" />
        </>
      )}
    </span>
  );
}

export function TrackIsAnalyzedCell(props: CellContext<LibraryTrack, boolean>) {
  return (
    <span className={["text-xs"].join(" ")}>
      {props.getValue() ? (
        <i className="i-ri-check-line text-green-500" />
      ) : (
        <>
          <i className="i-ri-close-line text-red-400" />
        </>
      )}
    </span>
  );
}

export function AlbumIsSyncedCell(props: CellContext<LibraryAlbum, boolean>) {
  return (
    <span className={["text-xs"].join(" ")}>
      {props.getValue() ? (
        <i className="i-ri-check-line text-green-500" />
      ) : (
        <>
          <i className="i-ri-close-line text-red-400" />
        </>
      )}
    </span>
  );
}
