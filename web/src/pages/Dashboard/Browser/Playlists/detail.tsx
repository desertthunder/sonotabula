import { Breadcrumbs } from "@/components/common/breadcrumbs";
import { usePlaylistAction } from "@/libs/hooks/mutations";
import type {
  BrowserPlaylistResponse,
  BrowserPlaylistTrack,
  Computations,
} from "@/libs/types/api";
import { useTokenStore } from "@/store";
import { useQuery } from "@tanstack/react-query";
import _, { toInteger } from "lodash";
import { useCallback, useEffect, useState } from "react";
import { useLocation, useParams, useSearch } from "wouter";
import { AverageRadialBarChart, SuperlativeBarChart } from "./charts";
import { formatDuration } from "@/libs/helpers";
import colors from "tailwindcss/colors";
import { TrackList } from "./trackList";

async function fetchBrowserPlaylist(
  id: string | undefined,
  token: string | null
) {
  const url = new URL(
    `/server/api/v1/browser/playlists/${id}`,
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
      <dd className={["flex items-center gap-1 p-1"].join(" ")}>
        {children ? children : value ? value : "None"}
      </dd>
    </>
  );
}

const radialFill = (attribute: keyof Computations["averages"]): string => {
  switch (attribute) {
    case "danceability":
      return colors.rose["500"];
    case "energy":
      return colors.orange["500"];
    case "loudness":
      return colors.emerald["500"];
    case "speechiness":
      return colors.sky["500"];
    case "acousticness":
      return colors.cyan["500"];
    case "instrumentalness":
      return colors.indigo["500"];
    case "liveness":
      return colors.fuchsia["500"];
    case "valence":
      return colors.violet["500"];
    case "tempo":
      return colors.amber["500"];
    case "duration_ms":
      return colors.stone["500"];
    default:
      return colors.green["500"];
  }
};

enum Views {
  Averages = "Averages",
  Superlatives = "Superlatives",
  Tracks = "Tracks",
}

function useQueryUrlParams(): [Views, (tab: Views) => void] {
  const search = useSearch();
  const [, setLocation] = useLocation();

  const changeTab = useCallback(
    (tab: Views) => {
      setLocation(`?tab=${tab.toLocaleLowerCase()}`);
    },
    [setLocation]
  );

  if (!search) {
    return [Views.Superlatives, changeTab];
  }

  const params = new URLSearchParams(search);
  // We're looking for the `tab` key in the query parameters
  // to determine the current scope of the dashboard table.
  if (!params.get("tab")) {
    return [Views.Superlatives, changeTab];
  }

  switch (params.get("tab")) {
    case "list":
    case "tracks":
      return [Views.Tracks, changeTab];
    case "avg":
    case "average":
    case "averages":
      return [Views.Averages, changeTab];
    case "super":
    case "minmax":
    case "superlatives":
    default:
      return [Views.Superlatives, changeTab];
  }
}
export function PlaylistDetailPage() {
  const { id } = useParams();
  const [pageQueryParams, onTabChange] = useQueryUrlParams();
  const query = useBrowserPlaylist();
  const syncMutation = usePlaylistAction(id, "sync");
  const analyzeMutation = usePlaylistAction(id, "analyze");
  const [isLoadingSync, setLoadingSync] = useState(false);
  const [isLoadingAnalysis, setLoadingAnalysis] = useState(false);
  const [isLoading, setLoading] = useState(false);
  const [view, setView] = useState<Views>(pageQueryParams);

  const refresh = useCallback(() => {
    if (query.isFetched && !query.isPending) {
      query.refetch();
    }
  }, [query]);

  useEffect(() => {
    if (query.isFetching) {
      setLoading(true);

      return;
    }

    const timeout = setTimeout(() => {
      setLoading(false);
    }, 1500);

    return () => {
      clearTimeout(timeout);
    };
  }, [query.isFetching]);

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

        lookups: new Map<string, BrowserPlaylistTrack>(
          tracks.map((track) => [track.id, track])
        ),
      };

  const radialData = _.isNil(computations)
    ? []
    : _.map(
        _.omit(computations.averages, ["duration_ms", "loudness", "tempo"]),
        (value, key) => {
          return {
            name: _.startCase(key),
            value: _.round(value, 3),
            fill: radialFill(key as keyof Computations["averages"]),
          };
        }
      );
  const otherData = _.isNil(computations)
    ? []
    : _.map(
        _.pick(computations.averages, ["duration_ms", "loudness", "tempo"]),
        (value, key) => {
          return {
            value: _.round(value, 3),
            name: (() => {
              switch (key) {
                case "duration_ms":
                  return "Duration (ms)";
                case "loudness":
                  return "Loudness";
                case "tempo":
                  return "Tempo";
                default:
                  return "";
              }
            })(),
          };
        }
      );

  return (
    <div className="flex flex-col w-full text-sm min-h-min bg-white">
      <section data-testid="search-bar" className="p-4 bg-white">
        <i className="i-ri-search-line" />
      </section>
      <Breadcrumbs title={playlist.name} context="playlists" />
      <section className="flex items-center border-y border-primary ">
        <div className="bg-primary aspect-square max-w-[250px] p-4 flex items-center">
          <img src={playlist.image_url} alt={playlist.name} />
        </div>

        <section className="flex flex-col border-x border-black h-full w-full">
          <header className="sticky text-base bg-primary pl-4 py-3 pr-8 flex items-center gap-1">
            <h1 className="text-white font-medium flex-1">Playlist Metadata</h1>
            <button
              className={[
                "bg-white text-emerald-600",
                "px-2 py-1 rounded-md",
                "hover:bg-zinc-100",
                "text-sm",
                "hover:scale-110",
                "transition-all duration-200 ease-in-out",
              ].join(" ")}
              onClick={refresh}
              disabled={isLoading}
            >
              <i
                className={[
                  query.isFetching ? "i-ri-loader-5-line animate-spin" : "",
                  "i-ri-refresh-line align-middle",
                ].join(" ")}
              />
            </button>
            <button
              className={[
                "bg-white text-primary",
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
                "text-primary bg-white",
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
          <dl className="bg-white grid grid-cols-4 flex-1 max-h-full lg:max-w-[75%] xl:max-w-[50%] overflow-y-auto overflow-x-hidden text-sm p-2 pl-4 pr-0">
            <Detail title="Name">
              <span>{playlist.name}</span>
            </Detail>
            <div className="sr-only">
              <Detail title="ID" value={playlist.id} />
            </div>
            <Detail title="Spotify URL">
              <a
                title={playlist.spotify_url}
                href={playlist.spotify_url}
                target="_blank"
                rel="noreferrer"
                className={[
                  "text-emerald-400 hover:text-green-700",
                  "transition-colors duration-200 ease-in-out",
                  "flex items-center",
                ].join(" ")}
              >
                <span className="mr-1 align-middle">Link</span>
                <i className="i-ri-spotify-fill" />
              </a>
            </Detail>
            <Detail title="Owner" value={playlist.owner_id} />
            <Detail title="Version">
              <span title={playlist.version}>
                {playlist.version.slice(
                  0,
                  toInteger(playlist.version.length / 3)
                )}
                ...
              </span>
            </Detail>
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
      <section className="flex items-center border-b" data-testid="tabs">
        {[Views.Superlatives, Views.Averages, Views.Tracks].map((v) => {
          return (
            <button
              key={v}
              className={[
                "border-b-2 p-4",
                view === v
                  ? "border-secondary pointer-events-none"
                  : "border-transparent hover:border-secondary",
              ].join(" ")}
              onClick={() => {
                setView(v);
                onTabChange(v);
              }}
              disabled={view === v}
            >
              {v}
            </button>
          );
        })}
      </section>
      {/* Charts */}
      {attrs ? (
        <main className="bg-white flex flex-col flex-1 overflow-auto p-4 gap-4">
          {view === Views.Tracks ? (
            <TrackList tracks={tracks} />
          ) : view === Views.Averages ? (
            <>
              <section className="grid grid-cols-3 border-b">
                {otherData.map((data) => (
                  <div key={data.name} className="p-4">
                    <h2 className="text-base">{data.name}</h2>
                    <p className="text-xs">{data.value}</p>
                    {data.name === "Duration (ms)" ? (
                      <p className="text-xs">
                        Formatted Duration:{" "}
                        {formatDuration(data.value as number)}
                      </p>
                    ) : null}
                  </div>
                ))}
              </section>
              <AverageRadialBarChart data={radialData} />
            </>
          ) : (
            <SuperlativeBarChart {...attrs} />
          )}
        </main>
      ) : null}
    </div>
  );
}
