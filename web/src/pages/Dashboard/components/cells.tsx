import { DrawerKey, useDrawerStore } from "@/store/drawers";
import type { LibraryPlaylist } from "@libs/types";
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

  return <button onClick={toggleFn}>{props.getValue()}</button>;
}
