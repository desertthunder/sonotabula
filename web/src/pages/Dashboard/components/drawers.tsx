import { formatDuration } from "@/libs/helpers";
import { useTokenStore } from "@/store";
import { DrawerKey, useDrawerStore } from "@/store/drawers";
import { LibraryKey } from "@libs/types";
import { useQuery } from "@tanstack/react-query";
import _ from "lodash";
import React, { useCallback, useEffect, useRef, useState } from "react";
import { useShallow } from "zustand/react/shallow";

// TODO: Move to common/libs
function useDrawer(drawerId: DrawerKey) {
  const meta = useDrawerStore(
    useShallow((state) => ({
      isOpen: state.drawers[drawerId],
      toggleFn: state.toggleDrawer,
    }))
  );

  const ref = useRef<HTMLDivElement>(null);

  const toggle = useCallback(() => {
    meta.toggleFn(drawerId);
  }, [meta, drawerId]);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (ref.current && !ref.current.contains(event.target as Node)) {
        toggle();
      }
    }

    if (meta.isOpen) {
      document.addEventListener("mousedown", handleClickOutside);
    }

    return () => {
      // Unbind the event listener on clean up
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [ref, meta, toggle]);

  return { meta, ref, toggle };
}

async function fetchPlaylist(key: DrawerKey, token: string | null) {
  if (!token) {
    return;
  }

  const queryKey = key.split("-");
  const id = _.last(queryKey);

  const uri = new URL(`api/v1/library/playlists/${id}`, window.location.origin);

  const res = await fetch(uri.toString(), {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!res.ok) {
    throw new Error(
      `Request failed with status: ${res.status} | ${res.statusText}`
    );
  }

  return await res.json();
}

async function fetchTrack(key: DrawerKey, token: string | null) {
  if (!token) {
    return;
  }

  const queryKey = key.split("-");
  const id = _.last(queryKey);

  const uri = new URL(`api/v1/library/tracks/${id}`, window.location.origin);

  const res = await fetch(uri.toString(), {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!res.ok) {
    throw new Error(
      `Request failed with status: ${res.status} | ${res.statusText}`
    );
  }

  return await res.json();
}

async function fetchTrackAnalysis(key: DrawerKey, token: string | null) {
  if (!token) {
    return;
  }

  const queryKey = key.split("-");
  const id = _.last(queryKey);

  const uri = new URL(
    `api/v1/library/tracks/${id}/analysis`,
    window.location.origin
  );

  const res = await fetch(uri.toString(), {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!res.ok) {
    throw new Error(
      `Request failed with status: ${res.status} | ${res.statusText}`
    );
  }

  return await res.json();
}

// TODO: Move to common/components
function DrawerLoader() {
  return (
    <div className="h-full flex flex-col gap-2 items-center justify-center">
      <span>Loading</span>
      <i className="i-ri-loader-line animate-spin text-2xl"></i>
    </div>
  );
}

// TODO: Move to common/components
function DrawerError() {
  return (
    <div className="h-full flex flex-col gap-2 items-center justify-center">
      <span>Error</span>
      <i className="i-ri-error-warning-line text-2xl"></i>
    </div>
  );
}

// TODO: Move to common/components
function KeyValue({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <>
      <dt className="font-semibold col-span-1">{title}</dt>
      <dd className="col-span-2 overflow-clip overflow-ellipsis">{children}</dd>
    </>
  );
}

// TODO:" Move to common/components"
function KeyValueList({
  children,
  colSpan,
}: {
  children: React.ReactNode;
  colSpan?: number;
}) {
  return (
    <dl
      className={`grid grid-cols-3 gap-1 p-2 ${
        colSpan ? `col-span-${colSpan}` : ""
      }`}
    >
      {children}
    </dl>
  );
}

// TODO:" Move to common/components"
function DrawerHeader({
  title,
  handler,
}: {
  title: string;
  handler: () => void;
}) {
  return (
    <header className="p-4 flex justify-between items-center border-b bg-emerald-500">
      <h1 className="text-lg font-semibold text-zinc-50">{title}</h1>
      <button
        className="bg-zinc-50 font-medium text-red-400 hover:text-zinc-50 hover:bg-red-400 border rounded-lg px-2 py-1 text-sm"
        onClick={handler}
      >
        Close
      </button>
    </header>
  );
}

// TODO:" Move to common/components"
function DrawerContent({ children }: { children: React.ReactNode }) {
  return (
    <main className="text-sm font-titles tracking-tight leading-tight font-medium">
      {children}
    </main>
  );
}

// TODO: Move to common/components
function Cover({ url }: { url: string }) {
  return <img src={url} alt="Cover" className="col-span-2 p-2" />;
}

interface DrawerProps {
  children?: React.ReactNode;
  drawerId: DrawerKey;
  token: string | null;
}

export function LibraryPlaylistDrawer({
  children,
  drawerId,
  token,
}: DrawerProps) {
  const queryKey = drawerId.split("-");

  const query = useQuery({
    queryKey,
    queryFn: async () => fetchPlaylist(drawerId, token),
    enabled: false,
    retry: 2,
  });

  const { meta, ref, toggle } = useDrawer(drawerId);

  useEffect(() => {
    if (meta.isOpen) {
      query.refetch();
    }
  }, [meta.isOpen, query]);

  return (
    <div
      data-drawer-id={drawerId}
      className={[
        `fixed inset-0 z-50`,
        `${meta.isOpen ? "translate-x-0" : "translate-x-full"}`,
        `transition-all`,
        `duration-300`,
        meta.isOpen ? `bg-opacity-75` : "bg-opacity-0",
        `bg-gray-800`,
      ].join(" ")}
    >
      <div
        ref={ref}
        className={`fixed right-0 top-0 bottom-0 w-96 bg-white shadow-lg transition-transform transform ${
          meta.isOpen ? "translate-x-0" : "translate-x-full"
        }`}
      >
        <DrawerHeader title="Playlist Details" handler={toggle} />

        {query.isLoading ? <DrawerLoader /> : null}
        {query.isError ? <DrawerError /> : null}
        {query.isSuccess ? (
          <DrawerContent>
            <section className="grid grid-cols-5 gap-2 border-b">
              <Cover url={query.data.image_url} />
              <KeyValueList colSpan={3}>
                <KeyValue title="ID">{query.data.spotify_id}</KeyValue>
                <KeyValue title="Name">{query.data.name}</KeyValue>
                <KeyValue title="URI">
                  <a
                    href={`https://open.spotify.com/playlist/${query.data.spotify_id}`}
                    target="_blank"
                    rel="noreferrer"
                  >
                    Link
                  </a>
                </KeyValue>
                <KeyValue title="Shared">
                  {query.data.shared ? "Yes" : "No"}
                </KeyValue>
                <KeyValue title="Public">
                  {query.data.collaborative ? "Yes" : "No"}
                </KeyValue>
              </KeyValueList>
            </section>
            <section>
              <header className="p-4 border-b flex justify-between items-center">
                <h2 className="text-lg font-semibold">Tracks</h2>
                <h3>
                  <strong>Total:</strong> {query.data.tracks.length}
                </h3>
              </header>
              <div className="overflow-x-auto flex flex-col divide-y">
                {query.data.tracks.map((track: any) => (
                  <dl key={track.id} className="grid grid-cols-3 gap-1 p-4">
                    <dt className="font-semibold col-span-1">Artist</dt>
                    <dd className="col-span-2 overflow-clip overflow-ellipsis">
                      {track.artists.map(([_id, name]: Array<string>) => (
                        <span key={_id}>{name}</span>
                      ))}
                    </dd>

                    <dt className="font-semibold col-span-1">Name</dt>
                    <dd className="col-span-2 overflow-clip overflow-ellipsis">
                      {track.name}
                    </dd>

                    <dt className="font-semibold col-span-1">URI</dt>
                    <dd className="col-span-2">
                      <a href={track.uri} target="_blank" rel="noreferrer">
                        Link
                      </a>
                    </dd>
                  </dl>
                ))}
              </div>
            </section>
          </DrawerContent>
        ) : null}
        {children}
      </div>
    </div>
  );
}

export function Stack({
  data,
}: {
  data: Record<string | number, string | number>;
}) {
  const cleanTitle = (title: string) =>
    title
      .split("_")
      .map((word) => {
        if (word.length > 2) {
          return word.charAt(0).toUpperCase() + word.slice(1);
        }

        return `(${word})`;
      })
      .join(" ");

  return (
    <>
      <header className="border-b shadow-lg">
        <h3 className="text-lg font-semibold p-4">Track Features</h3>
      </header>
      <section className="flex flex-col divide-y font-medium font-headings max-h-[600px] overflow-y-scroll">
        {Object.entries(data).map(([key, value]) => {
          if (key === "id") return null;

          return (
            <div key={key} className="grid grid-rows-2 gap-2 py-2 px-4">
              <div className="text-right font-semibold">{cleanTitle(key)}</div>
              <div className="text-right">{value}</div>
            </div>
          );
        })}
      </section>
    </>
  );
}

export function LibraryTrackDrawer({ drawerId, token }: DrawerProps) {
  const queryKey = drawerId.split("-");
  const query = useQuery({
    queryKey,
    queryFn: async () => fetchTrack(drawerId, token),
    enabled: false,
    retry: 2,
  });

  const { meta, ref, toggle } = useDrawer(drawerId);

  const analysisQuery = useQuery({
    queryKey: [...queryKey, "analysis"],
    queryFn: async () => fetchTrackAnalysis(drawerId, token),
    enabled: false,
    retry: 2,
  });

  useEffect(() => {
    if (meta.isOpen) {
      query.refetch();
    }
  }, [meta.isOpen, query]);

  useEffect(() => {
    if (meta.isOpen && query.data && query.data.is_analyzed) {
      analysisQuery.refetch();
    }
  }, [meta.isOpen, query.data, analysisQuery]);

  return (
    <div
      data-drawer-id={drawerId}
      className={[
        `fixed inset-0 z-50`,
        `${meta.isOpen ? "translate-x-0" : "translate-x-full"}`,
        `transition-all`,
        `duration-300`,
        meta.isOpen ? `bg-opacity-75` : "bg-opacity-0",
        `bg-gray-800`,
      ].join(" ")}
    >
      <div
        ref={ref}
        className={`fixed right-0 top-0 bottom-0 w-96 bg-white shadow-lg transition-transform transform ${
          meta.isOpen ? "translate-x-0" : "translate-x-full"
        }`}
      >
        <DrawerHeader title="Track Details" handler={toggle} />
        {query.isLoading ? <DrawerLoader /> : null}
        {query.isError ? <DrawerError /> : null}
        {query.isSuccess ? (
          <DrawerContent>
            <section className="grid grid-cols-5 gap-2 border-b">
              <Cover url={query.data.image_url} />
              <KeyValueList colSpan={3}>
                <KeyValue title="Name">
                  <span>{query.data.name}</span>
                </KeyValue>
                {/* Arist Name */}
                <KeyValue title="Artist">{query.data.artist_name}</KeyValue>
                {/* Album Name */}
                <KeyValue title="Album">{query.data.album_name}</KeyValue>
                {/* Duration */}

                {/* Duration (ms) */}
                <KeyValue title="Length">
                  {formatDuration(query.data.duration_ms)}
                </KeyValue>
                {/* Is Synced? */}
                <KeyValue title="Synced?">
                  {query.data.is_synced ? "Yes" : "No"}
                </KeyValue>
                {/* Is Analyzed? */}
                <KeyValue title="Analyzed?">
                  {query.data.is_analyzed ? "Yes" : "No"}
                </KeyValue>
              </KeyValueList>
            </section>
            {query.data.is_analyzed ? (
              <>
                {analysisQuery.isLoading ? <DrawerLoader /> : null}
                {analysisQuery.isError ? <DrawerError /> : null}
                {analysisQuery.isSuccess ? (
                  <Stack data={analysisQuery.data} />
                ) : null}
              </>
            ) : null}
          </DrawerContent>
        ) : null}
      </div>
    </div>
  );
}

interface DrawersProps {
  scope: LibraryKey;
  ids: string[];
}

export function Drawers({ scope, ids }: DrawersProps) {
  const drawerKeys = ids.map((id) => `${scope}-${id}` as DrawerKey);
  const [registered, setRegistered] = useState(false);
  const { registerBatch } = useDrawerStore(
    useShallow((state) => ({ registerBatch: state.registerBatch }))
  );
  const token = useTokenStore((state) => state.token);

  useEffect(() => {
    if (drawerKeys.length > 0) {
      registerBatch(drawerKeys);
      setRegistered(true);
    }
  }, [registerBatch, drawerKeys]);

  if (registered) {
    return drawerKeys.map((k) => {
      switch (scope) {
        case LibraryKey.LibraryPlaylists:
          return <LibraryPlaylistDrawer key={k} drawerId={k} token={token} />;
        case LibraryKey.LibraryTracks:
          return <LibraryTrackDrawer key={k} drawerId={k} token={token} />;
        default:
          return null;
      }
    });
  } else {
    return null;
  }
}
