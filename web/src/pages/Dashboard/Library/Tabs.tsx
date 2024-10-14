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
    <div className="mb-4">
      {RESOURCE_KEYS.map((resource) => {
        return (
          <button
            key={resource}
            onClick={onChange.bind(null, resource)}
            // className={scope === resource ? "active" : ""}
            className={[
              "px-4 py-2",
              "text-sm font-semibold",
              "text-zinc-100",
              "cursor-pointer",
              "hover:text-white",
              "hover:bg-emerald-500",
              "focus:outline-none",
              "focus:ring-2 focus:ring-emerald-500",
              "focus:ring-offset-2 focus:ring-offset-zinc-100",
              "transition-all",
              scope === resource ? "pointer-events-none bg-emerald-500" : "",
            ].join(" ")}
            disabled={scope === resource}
            value={resource}
          >
            {textMap[resource]}
          </button>
        );
      })}
    </div>
  );
}
