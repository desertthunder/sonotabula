import { ResourceKey } from "@/libs/hooks";
import { RESOURCE_KEYS } from "@/libs/hooks/fetch";
import { Dispatch, SetStateAction } from "react";

type TabState = [ResourceKey, Dispatch<SetStateAction<ResourceKey>>];

interface TabsProps {
  current: TabState;
}

const textMap = {
  [ResourceKey.LibraryPlaylists]: "Playlists",
  [ResourceKey.LibraryTracks]: "Tracks",
  [ResourceKey.LibraryAlbums]: "Albums",
  [ResourceKey.LibraryArtists]: "Artists",
} as const;

export function Tabs({ current }: TabsProps) {
  const [tab, setTab] = current;

  return (
    <nav>
      {RESOURCE_KEYS.map((resource) => {
        return (
          <button
            key={resource}
            onClick={() => setTab(resource)}
            className={tab === resource ? "active" : ""}
            disabled={tab === resource}
          >
            {textMap[resource]}
          </button>
        );
      })}
    </nav>
  );
}
