import { LibraryKey, LibraryKeys, LibraryTitles } from "@libs/types";
import { UseMutationResult } from "@tanstack/react-query";
import { useEffect, useState } from "react";

interface Props {
  scope: LibraryKey;
  onChange: (key: LibraryKey) => void;
  context: UseMutationResult<any>;
}

export function Tabs({ scope, onChange, context }: Props) {
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (context.isPending) {
      setIsLoading(true);
      return;
    }

    const timeout = setTimeout(() => {
      setIsLoading(false);
    }, 1000);

    return () => clearTimeout(timeout);
  }, [context.isPending]);

  const isDisabled = (resource: LibraryKey) => {
    if (isLoading) return true;

    if (scope === resource) return true;

    if (scope === LibraryKey.LibraryArtists) return true;

    return false;
  };

  return (
    <div className="mt-4 mb-2 gap-x-2 flex items-start justify-between">
      <div className="flex gap-x-2">
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
                "hover:bg-emerald-400",
                "rounded-lg",
                "flex items-center gap-2",
                "focus:outline-none",
                "focus:ring-2 focus:ring-emerald-500",
                "focus:ring-offset-2 focus:ring-offset-zinc-100",
                "transition-all",
                "group",
                "group:transition-transform group:duration-300",
                isDisabled(resource) ? "pointer-events-none" : "",
                scope === resource ? "bg-emerald-700" : "bg-emerald-500",
              ].join(" ")}
              disabled={isDisabled(resource)}
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
      <div>
        <button
          className={[
            "bg-white text-emerald-600",
            "rounded-lg p-2 flex items-center gap-2",
            "hover:bg-emerald-100",
            "hover:scale-110 hover:shadow-lg",
            "transition-transform duration-200",
            "group",
            [LibraryKey.LibraryAlbums, LibraryKey.LibraryArtists].includes(
              scope
            )
              ? "pointer-events-none bg-zinc-200"
              : "",
          ].join(" ")}
          disabled={[
            LibraryKey.LibraryAlbums,
            LibraryKey.LibraryArtists,
          ].includes(scope)}
          onClick={() => context.mutate(undefined)}
        >
          {isLoading ? (
            <i className="i-ri-loader-2-fill animate-spin" />
          ) : (
            <i className="i-ri-refresh-line group-hover:rotate-45" />
          )}
          <span>Sync</span>
          <span className="sr-only">Sync Current Library Page</span>
        </button>
      </div>
    </div>
  );
}
