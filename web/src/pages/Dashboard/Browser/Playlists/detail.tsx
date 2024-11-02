import { useParams } from "wouter";
import { Breadcrumbs } from "@/components/common/breadcrumbs";
import { useQuery } from "@tanstack/react-query";
import { useTokenStore } from "@/store";
import type {
  BrowserPlaylistResponse,
  BrowserPlaylistTrack,
} from "@/libs/types/api";
import { BarChart } from "./charts";
import { usePlaylistAction } from "@/libs/hooks/mutations";
import _ from "lodash";
import { useEffect, useState } from "react";

async function fetchBrowserPlaylist(
  id: string | undefined,
  token: string | null
) {
  const url = new URL(
    `/api/v1/browser/playlists/${id}`,
    window.location.origin
  );
  const response = await fetch(url.toString(), {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch playlist");
  }

  return (await response.json()) as BrowserPlaylistResponse;
}

function useBrowserPlaylist() {
  const { id } = useParams();
  const token = useTokenStore((state) => state.token);

  const query = useQuery({
    queryKey: ["browser", "playlists", id],
    queryFn: () => fetchBrowserPlaylist(id, token),
  });

  return query;
}

function Detail({
  title,
  value,
  children,
}: {
  title: string;
  value?: string;
  children?: React.ReactNode;
}) {
  return (
    <>
      <dt className={["font-bold flex items-center"].join(" ")}>{title}</dt>
      <dd
        className={[
          "flex items-center gap-1 p-1",
          ["Version", "Owner", "Spotify URL"].includes(title) ? "blur-sm" : "",
        ].join(" ")}
      >
        {children ? children : value ? value : "None"}
      </dd>
    </>
  );
}

export function PlaylistDetailPage() {
  const { id } = useParams();
  const query = useBrowserPlaylist();
  const syncMutation = usePlaylistAction(id, "sync");
  const analyzeMutation = usePlaylistAction(id, "analyze");
  const [isLoadingSync, setLoadingSync] = useState(false);
  const [isLoadingAnalysis, setLoadingAnalysis] = useState(false);

  useEffect(() => {
    if (syncMutation.isPending) {
      setLoadingSync(true);

      return;
    }

    const timeout = setTimeout(() => {
      setLoadingSync(false);
    }, 1500);

    return () => {
      clearTimeout(timeout);
    };
  }, [syncMutation.isPending]);

  useEffect(() => {
    if (analyzeMutation.isPending) {
      setLoadingAnalysis(true);

      return;
    }

    const timeout = setTimeout(() => {
      setLoadingAnalysis(false);
    }, 1500);

    return () => {
      clearTimeout(timeout);
    };
  }, [analyzeMutation.isPending]);

  if (query.isLoading) {
    return <div>Loading...</div>;
  }

  if (query.isError) {
    return <div>Error: {query.error.message}</div>;
  }

  if (!query.data) {
    return <div>No data</div>;
  }

  const { playlist, computations, tracks } = query.data.data;
  const attrs = _.isNil(computations)
    ? null
    : {
        data: computations.superlatives,
        cleaned: _.omit(computations.superlatives, [
          "duration_ms",
          "loudness",
          "tempo",
        ]),
        labels: _.keys(
          _.omit(computations.superlatives, [
            "duration_ms",
            "loudness",
            "tempo",
          ])
        ).map((key) => _.startCase(key)),
        lookups: new Map<string, BrowserPlaylistTrack>(
          tracks.map((track) => [track.id, track])
        ),
      };

  return (
    <div className="flex flex-col w-full text-sm min-h-min bg-white">
      <section data-testid="search-bar" className="p-4 bg-white">
        <i className="i-ri-search-line" />
      </section>
      <Breadcrumbs title={playlist.name} />
      <section className="flex items-center border-y border-emerald-500 ">
        <div className="bg-emerald-500 aspect-square max-w-[250px] p-4 flex items-center">
          <img src={playlist.image_url} alt={playlist.name} />
        </div>

        <section className="flex flex-col border-x border-black max-h-[250px] w-full">
          <header className="sticky text-base bg-emerald-500 pl-4 py-3 pr-8 flex items-center gap-1">
            <h1 className="text-white font-medium flex-1">Playlist Metadata</h1>
            <button
              className={[
                "bg-white text-emerald-500",
                "px-2 py-1 rounded-md",
                "hover:bg-zinc-100",
                "text-sm",
                "hover:scale-110",
                "transition-all duration-200 ease-in-out",
              ].join(" ")}
              onClick={() => syncMutation.mutate()}
              disabled={isLoadingSync || isLoadingAnalysis}
            >
              {isLoadingSync ? (
                <i className="i-ri-loader-line animate-spin" />
              ) : (
                "Sync"
              )}
            </button>
            <button
              className={[
                "text-emerald-500 bg-white",
                "px-2 py-1 rounded-md",
                "text-sm",
                "hover:bg-zinc-100",
                "hover:scale-110",
                "transition-all duration-200 ease-in-out",
              ].join(" ")}
              onClick={() => analyzeMutation.mutate()}
              disabled={isLoadingAnalysis || isLoadingSync}
            >
              {isLoadingAnalysis ? (
                <i className="i-ri-loader-line animate-spin" />
              ) : (
                "Analyze"
              )}
            </button>
          </header>
          <dl className="bg-white grid grid-cols-2 verflow-y-auto overflow-x-hidden text-sm p-2 pl-4 pr-0">
            <Detail title="Name">
              <span>{playlist.name}</span>
              <a
                href={playlist.spotify_url}
                target="_blank"
                rel="noreferrer"
                className={[
                  "text-emerald-400 hover:text-green-700",
                  "transition-colors duration-200 ease-in-out",
                  "flex items-center p-1",
                ].join(" ")}
              >
                <i className="i-ri-spotify-fill" />
              </a>
            </Detail>
            <div className="sr-only">
              <Detail title="ID" value={playlist.id} />
            </div>
            <Detail title="Spotify URL" value={playlist.spotify_url} />
            <Detail title="Owner" value={playlist.owner_id} />
            <Detail title="Version" value={playlist.version} />
            <Detail title="Public" value={playlist.public ? "Yes" : "No"} />
            <Detail title="Shared" value={playlist.shared ? "Yes" : "No"} />
            <Detail title="Synced" value={playlist.is_synced ? "Yes" : "No"} />
            <Detail
              title="Analyzed"
              value={playlist.is_analyzed ? "Yes" : "No"}
            />
            <Detail
              title="Description"
              value={playlist.description || "None"}
            />
          </dl>
        </section>
      </section>

      {/* Charts */}
      {attrs ? (
        <main className="bg-white flex flex-col flex-1 overflow-auto">
          <BarChart {...attrs} />
        </main>
      ) : null}
    </div>
  );
}
