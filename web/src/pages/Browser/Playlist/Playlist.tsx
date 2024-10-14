import { usePlaylistTracks } from "@/libs/hooks";
import React, { useCallback, useMemo } from "react";
import { useMatch, useNavigate, useParams } from "react-router-dom";
import { Drawer } from "vaul";

type Playlist = {
  id: string;
  name: string;
  album_name: string;
  is_analyzed: boolean;
  is_synced: boolean;
  image_url: string;
  tracks: {
    id: string;
    name: string;
    album_name: string;
    features: Record<string, string>;
  }[];
};

function translateKey(key: string) {
  const title = key.charAt(0).toUpperCase() + key.slice(1);

  if (title === "Duration_ms") {
    return "Duration";
  }

  if (title === "Time_signature") {
    return "Time Signature";
  }

  return title.replace(/_/g, " ");
}

function keyToPitchClass(key: number) {
  const pitchClasses = [
    "C",
    "C♯",
    "D",
    "D♯",
    "E",
    "F",
    "F♯",
    "G",
    "G♯",
    "A",
    "A♯",
    "B",
  ];

  return pitchClasses[key];
}

function parseValue(key: string, value: string | number): string {
  switch (key) {
    case "key":
      return keyToPitchClass(value as number);
    case "tempo":
      return `${value} BPM`;
    case "loudness":
      return `${value} dB`;
    case "time_signature":
      return `${value} / 4`;
    case "duration_ms":
      return translateDuration(value as number);
    default:
      return value as string;
  }
}

function translateDuration(duration_ms: number | string) {
  const ms = parseInt(duration_ms as string);
  const minutes = Math.floor(ms / 60000);
  const seconds = ((ms % 60000) / 1000).toFixed(0);

  return `${minutes}:${+seconds < 10 ? "0" : ""}${seconds}`;
}

/**
 * @todo - make a hook to generate a description list
 * @todo - meta properties - name, album_name, artist_name
 * @todo - traits - all of features
 */
export function Playlist() {
  const match = useMatch("/dashboard/browser/playlists/:id");
  const params = useParams();
  const navigate = useNavigate();
  const query = usePlaylistTracks(params.id as string);

  const isOpen = useMemo(() => {
    return !!match;
  }, [match]);

  const onOpenChange = useCallback(
    (open: boolean) => {
      if (!open) {
        navigate("/dashboard/browser/playlists");
      }
    },
    [navigate]
  );

  if (query.isLoading) {
    return <div>Loading...</div>;
  }

  if (query.isError) {
    return <div>Error: {query.error.message}</div>;
  }

  return (
    <Drawer.Root direction="right" open={isOpen} onOpenChange={onOpenChange}>
      <Drawer.Portal>
        <Drawer.Overlay className="fixed inset-0 bg-black/40" />
        <Drawer.Content className="right-0 top-12 bottom-0 fixed z-10 flex outline-none">
          <div className="bg-zinc-50 rounded-md w-1/2 grow mt-2 mr-2 mb-2 p-5 flex flex-col">
            <div className="max-w-md mx-auto overflow-y-auto flex-1">
              {query.isSuccess && query.data ? (
                <>
                  <Drawer.Title className="font-medium mb-4  flex flex-row justify-between">
                    <div className="flex justify-between gap-x-1 items-center w-full flex-row-reverse">
                      <img
                        src={query.data.playlist.image_url}
                        className="w-8 h-8"
                        alt="Playlist Cover"
                      />
                      <h1 className="text-zinc-900 text-lg">
                        {query.data.playlist.name}
                      </h1>
                    </div>

                    <div className="flex flex-shrink-0 gap-x-2 ml-2">
                      {query.data.tracks.length === 0 ? (
                        <button className="bg-emerald-300 hover:bg-emerald-400 text-grey-900 py-1 px-4 rounded-lg inline-flex items-center text-xs">
                          Analyze
                        </button>
                      ) : null}

                      {!query.data.playlist.is_analyzed ? (
                        <button className="bg-sky-300 hover:bg-sky-400 text-grey-900 py-1 px-4 rounded-lg inline-flex items-center text-xs">
                          Sync
                        </button>
                      ) : (
                        <button className="bg-sky-300 hover:bg-sky-400 text-grey-900 py-1 px-4 rounded-lg inline-flex items-center text-xs">
                          Resync
                        </button>
                      )}
                    </div>
                  </Drawer.Title>
                  <Drawer.Description className="font-medium text-zinc-600 ">
                    Track List
                  </Drawer.Description>
                  {/* @ts-expect-error any */}
                  {query.data.tracks.map((track) => (
                    <section
                      className="border-b border-b-zinc-300 py-4 first:pt-0"
                      key={track.id}
                    >
                      <dd className="grid grid-cols-3 gap-2">
                        <dl className="py-2" key={track.id}>
                          <dt className="font-semibold text-sm leading-7 text-gray-900">
                            Title
                          </dt>
                          <dd className="mt-1 text-xs leading-6 text-gray-500">
                            {track.name}
                          </dd>
                        </dl>
                        <dl className="py-2">
                          <dt className="font-semibold text-sm leading-7 text-gray-900">
                            Album
                          </dt>
                          <dd className="mt-1 text-xs leading-6 text-gray-500">
                            {track.album_name}
                          </dd>
                        </dl>
                        <dl className="py-2">
                          <dt className="font-semibold text-sm leading-7 text-gray-900">
                            Artist
                          </dt>
                          <dd className="mt-1 text-xs leading-6 text-gray-500">
                            <em>Placeholder</em>
                          </dd>
                        </dl>
                      </dd>
                      {track.features ? (
                        <dl className="py-2">
                          <dt className="font-semibold leading-7 text-zinc-600">
                            Features
                          </dt>
                          <dd className="mt-1 text-sm leading-6 text-gray-500">
                            <dl className="grid grid-cols-2 gap-2">
                              {Object.entries(track.features).map(
                                ([key, value]) => (
                                  <React.Fragment key={`${track.id}-${key}`}>
                                    {key === "id" ? null : (
                                      <React.Fragment>
                                        <dt className="font-semibold text-sm leading-7 text-gray-900">
                                          {translateKey(key)}
                                        </dt>
                                        <dd className="mt-1 text-xs leading-6 text-gray-500">
                                          {parseValue(key, value as string)}
                                        </dd>
                                      </React.Fragment>
                                    )}
                                  </React.Fragment>
                                )
                              )}
                            </dl>
                          </dd>
                        </dl>
                      ) : null}
                    </section>
                  ))}
                </>
              ) : null}
            </div>
          </div>
        </Drawer.Content>
      </Drawer.Portal>
    </Drawer.Root>
  );
}
