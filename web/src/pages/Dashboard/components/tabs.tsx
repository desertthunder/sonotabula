import { LibraryKey, LibraryKeys, LibraryTitles } from "@/libs/types";

interface Props {
  scope: LibraryKey;
  onChange: (key: LibraryKey) => void;
}

export function Tabs({ scope, onChange }: Props) {
  return (
    <div className="mb-4 gap-x-2 flex">
      {LibraryKeys.map((resource) => {
        return (
          <button
            key={resource}
            onClick={onChange.bind(null, resource)}
            // className={scope === resource ? "active" : ""}
            className={[
              "px-4 py-2",
              "text-sm font-semibold",
              "text-white",
              "cursor-pointer",
              "hover:text-white",
              "hover:bg-emerald-500",
              "rounded-lg",
              "flex items-center gap-2",
              "focus:outline-none",
              "focus:ring-2 focus:ring-emerald-500",
              "focus:ring-offset-2 focus:ring-offset-zinc-100",
              "transition-all",
              "group",
              "group:transition-transform group:duration-300",
              scope === resource ? "pointer-events-none bg-emerald-500" : "",
            ].join(" ")}
            disabled={scope === resource}
            value={resource}
          >
            {resource === LibraryKey.LibraryPlaylists ? (
              <i className="i-ri-play-list-2-fill group-hover:rotate-45" />
            ) : null}
            {resource === LibraryKey.LibraryTracks ? (
              <i className="i-ri-music-fill group-hover:rotate-45" />
            ) : null}
            {resource === LibraryKey.LibraryAlbums ? (
              <i className="i-ri-album-fill group-hover:rotate-45" />
            ) : null}
            {resource === LibraryKey.LibraryArtists ? (
              <i className="i-ri-user-2-fill group-hover:rotate-45" />
            ) : null}
            {LibraryTitles[resource]}
          </button>
        );
      })}
    </div>
  );
}
