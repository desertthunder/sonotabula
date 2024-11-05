import { BrowserPlaylistTrack } from "@/libs/types/api";
import { Fragment } from "react/jsx-runtime";
import _ from "lodash";
import { formatDuration, formatHeader } from "@/libs/helpers";

import Fuse from "fuse.js";
import { useCallback, useState } from "react";

function useFuzzySearch<T>(data: T[], keys: (keyof T)[]) {
  const fuse = new Fuse(data, {
    keys: keys as string[],
    includeScore: true,
  });

  return (query: string) => fuse.search(query).map((result) => result.item);
}

export function TrackList({ tracks }: { tracks: BrowserPlaylistTrack[] }) {
  const search = useFuzzySearch<BrowserPlaylistTrack>(tracks, [
    "artists",
    "name",
    "album_name",
  ]);

  const [query, setQuery] = useState("");

  const [filteredTracks, setFilteredTracks] =
    useState<BrowserPlaylistTrack[]>(tracks);

  const handleSearch = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const q = e.target.value;

      setQuery(q);

      if (!q) {
        setFilteredTracks(tracks);
        return;
      }

      const filtered = search(q);

      setFilteredTracks(filtered);
    },
    [search, tracks]
  );

  return (
    <Fragment>
      <div className="h-16">
        <input
          type="search"
          placeholder="Search for a track..."
          className="w-full rounded shadow-lg p-3 ring-1 ring-gray-300 focus:ring-emerald-400 focus:outline-none"
          value={query}
          onChange={handleSearch}
        />
      </div>
      {filteredTracks.map((track) => (
        <div
          className="grid grid-cols-12 gap-4 p-4 border rounded shadow-lg"
          key={track.id}
        >
          <div className="col-span-4 flex gap-2 text-sm font-sans font-medium">
            <img
              src={track.album_art}
              alt={track.name}
              className="w-32 h-32 col-span-3"
            />
            <div className="flex flex-col gap-1">
              <span>{track.name}</span>
              <span>{formatDuration(track.duration)}</span>
              <span>{track.album_name}</span>
              <span>{track.artists.map((a) => a.name).join(", ")}</span>
              <a
                href={`https://open.spotify.com/track/${track.spotify_id}`}
                target="_blank"
                rel="noreferrer"
                className="text-emerald-400 hover:text-green-700 transition-colors duration-200 ease-in-out"
              >
                <span className="mr-1 align-middle">Link</span>
                <i className="i-ri-spotify-fill align-middle" />
              </a>
            </div>
          </div>
          <dl className="col-span-8 grid grid-cols-6 gap-1 flex-1 text-xs">
            {_.map(track.features, (value, key) => (
              <Fragment key={key}>
                <dt className="font-bold text-left col-span-1">
                  {formatHeader(key)}
                </dt>
                <dd
                  className="font-medium col-span-2 text-left"
                  title={value as string}
                >
                  {key === "id" ? (value as string).slice(0, 5) + "..." : value}
                </dd>
              </Fragment>
            ))}
          </dl>
        </div>
      ))}
    </Fragment>
  );
}
