import { ResourceKey, RESOURCE_KEYS } from "@/libs/types";

interface Props {
  scope: ResourceKey;
  onChange: (key: ResourceKey) => void;
}

const textMap = {
  [ResourceKey.LibraryPlaylists]: "Playlists",
  [ResourceKey.LibraryTracks]: "Tracks",
  [ResourceKey.LibraryAlbums]: "Albums",
  [ResourceKey.LibraryArtists]: "Artists",
} as const;

export function Tabs({ scope, onChange }: Props) {
  return (
    <nav>
      {RESOURCE_KEYS.map((resource) => {
        return (
          <button
            key={resource}
            onClick={onChange.bind(null, resource)}
            className={scope === resource ? "active" : ""}
            disabled={scope === resource}
          >
            {textMap[resource]}
          </button>
        );
      })}
    </nav>
  );
}
