import { LibraryKey, LibraryKeys, LibraryTitles } from "@libs/types";
import { UseMutationResult } from "@tanstack/react-query";
import { useEffect, useState } from "react";

interface Props {
  scope: LibraryKey;
  onChange: (key: LibraryKey) => void;
  context: UseMutationResult<any>;
}

function getIconClassName(resource: LibraryKey) {
  switch (resource) {
    case LibraryKey.LibraryPlaylists:
      return "i-ri-play-list-2-fill";
    case LibraryKey.LibraryTracks:
      return "i-ri-music-fill";
    case LibraryKey.LibraryAlbums:
      return "i-ri-album-fill";
    case LibraryKey.LibraryArtists:
      return "i-ri-user-2-fill";
    default:
      return "i-ri-circle-fill";
  }
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
                "text-sm font-semibold text-white",
                "cursor-pointer",
                "rounded-lg",
                "flex items-center gap-2",
                "focus:outline-none",
                "focus:ring-2 focus:ring-primary",
                "focus:ring-offset-2 focus:ring-offset-zinc-100",
                "transition-all",
                "group group:transition-transform group:duration-300",
                isLoading ? "pointer-events-none" : "",
                scope === resource
                  ? "bg-emerald-700 pointer-events-none"
                  : "bg-primary hover:bg-emerald-600 hover:text-white",
              ].join(" ")}
              disabled={isLoading || scope === resource}
            >
              <i
                className={`${getIconClassName(
                  resource
                )} group-hover:rotate-45`}
              />

              {LibraryTitles[resource]}
            </button>
          );
        })}
      </div>
      <div>
        <button
          className={[
            "bg-white text-emerald-600 hover:bg-emerald-100",
            "rounded-lg p-2 flex items-center gap-2",
            "hover:scale-110 hover:shadow-lg",
            "transition-transform duration-200",
            "group",
            isLoading ? "pointer-events-none bg-zinc-200" : "",
          ].join(" ")}
          disabled={isLoading}
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
