import { humanReadableDate } from "@/libs/helpers";
import type { ListeningHistoryItem } from "@/libs/types";
import { useEffect, useMemo, useState } from "react";

interface Props {
  data: ListeningHistoryItem;
  refresh: () => void;
  isFetching: boolean;
}

export function LastPlayed({ data, refresh, isFetching }: Props) {
  const [showSpinner, setShowSpinner] = useState(false);
  const playedAt = useMemo(
    () => humanReadableDate(data.played_at),
    [data.played_at]
  );

  const links = useMemo(
    () => ({
      album: `https://open.spotify.com/album/${data.album.spotify_id}`,
      track: `https://open.spotify.com/track/${data.track.spotify_id}`,
    }),
    [data.album.spotify_id, data.track.spotify_id]
  );

  useEffect(() => {
    if (isFetching) {
      setShowSpinner(true);
    } else {
      setTimeout(() => {
        setShowSpinner(false);
      }, 1000);
    }
  }, [isFetching]);

  return (
    <div className="flex text-xs gap-2 items-start">
      <a
        href={links.album}
        target="_blank"
        rel="noreferrer"
        className="hover:ring-2 ring-green-500 rounded-sm"
      >
        {showSpinner ? (
          <div className="h-12 w-12 flex items-center justify-center ">
            <i className="i-ri-loader-line animate-spin text-green-500 text-xl" />
          </div>
        ) : (
          <img
            src={data.album.image_url}
            alt={data.album.name}
            className="max-h-12 max-w-12 rounded-sm"
          />
        )}
      </a>
      <div className="flex flex-col flex-1">
        <span className="text-slate-400 font-medium">Last Played</span>
        <a
          className="text-slate-800 hover:text-green-500"
          href={links.track}
          target="_blank"
          rel="noreferrer"
        >
          {data.track.name}
        </a>
        <span className="text-slate-500 text-xs">{playedAt}</span>
      </div>
      <div className="max-w-16 flex flex-col gap-1">
        <button
          aria-label="Refresh"
          className={[
            "text-emerald-500",
            "hover:bg-green-100",
            "hover:rounded-full",
            "hover:shadow-2xl",
            "px-1",
          ].join(" ")}
          onClick={refresh}
        >
          <i className="i-ri-refresh-line text-lg" />
        </button>
        <button
          disabled
          aria-label="History"
          className="pointer-events-none text-zinc-300"
        >
          <i className="i-ri-history-fill text-lg" />
        </button>
      </div>
    </div>
  );
}
