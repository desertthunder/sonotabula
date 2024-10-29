import { useTokenStore } from "@/store";
import { LibraryKey } from "@libs/types";
import { useQuery } from "@tanstack/react-query";
import React, { useCallback, useEffect, useRef, useState } from "react";
import { DrawerKey, useDrawerStore } from "@/store/drawers";
import _ from "lodash";
import { useShallow } from "zustand/react/shallow";

export function LibraryPlaylistDrawer({
  children,
  drawerId,
}: {
  drawerId: DrawerKey;
  children?: React.ReactNode;
}) {
  const meta = useDrawerStore(
    useShallow((state) => ({
      isOpen: state.drawers[drawerId],
      toggleFn: state.toggleDrawer,
    }))
  );

  const ref = useRef<HTMLDivElement>(null);

  const token = useTokenStore((state) => state.token);

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

  const queryKey = drawerId.split("-");

  const query = useQuery({
    queryKey,
    queryFn: async () => {
      const id = _.last(queryKey);
      const uri = new URL(
        `api/v1/library/playlists/${id}`,
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
    },
    enabled: false,
  });

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
        <header className="p-4 flex justify-between items-center border-b">
          <h1 className="text-lg font-semibold">Playlist Details</h1>
          <button
            className="text-gray-400 hover:text-zinc-50 hover:bg-red-400 border rounded-md px-2 py-1 text-sm"
            onClick={toggle}
          >
            Close
          </button>
        </header>
        <div>
          {query.isLoading ? (
            <div className="h-full flex flex-col gap-2 items-center justify-center">
              <span>Loading</span>
              <i className="i-ri-loader-line animate-spin text-2xl"></i>
            </div>
          ) : null}
          {query.isError ? "Error" : null}
          {query.isSuccess ? (
            <main className="text-sm font-titles tracking-tight leading-tight font-medium">
              <section className="grid grid-cols-5 gap-2 border-b">
                <img
                  src={query.data.image_url}
                  alt="Playlist Cover"
                  className="col-span-2 p-2"
                />
                <div className="col-span-3 p-2">
                  <dl className="grid grid-cols-3 gap-1">
                    <dt className="font-semibold col-span-1">ID</dt>
                    <dd className="col-span-2 overflow-clip overflow-ellipsis">
                      {query.data.spotify_id}
                    </dd>

                    <dt className="font-semibold col-span-1">Name</dt>
                    <dd className="col-span-2 overflow-clip overflow-ellipsis">
                      {query.data.name}
                    </dd>

                    <dt className="font-semibold col-span-1">URI</dt>
                    <dd className="col-span-2">
                      <a
                        href={`https://open.spotify.com/playlist/${query.data.spotify_id}`}
                        target="_blank"
                        rel="noreferrer"
                      >
                        Link
                      </a>
                    </dd>

                    {/* Shared */}
                    <dt className="font-semibold col-span-1">Shared</dt>
                    <dd className="col-span-2">
                      {query.data.shared ? "Yes" : "No"}
                    </dd>

                    {/* Public (collaborative prop) */}
                    <dt className="font-semibold col-span-1">Public</dt>
                    <dd className="col-span-2">
                      {query.data.collaborative ? "Yes" : "No"}
                    </dd>
                  </dl>
                </div>
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
              <footer></footer>
            </main>
          ) : null}
          {children}
        </div>
      </div>
    </div>
  );
}

type DrawerContainerProps = {
  r: Record<LibraryKey.LibraryPlaylists, DrawerKey[]>;
};

export function Drawers(props: DrawerContainerProps) {
  const [registered, setRegistered] = useState(false);
  const { registerBatch } = useDrawerStore(
    useShallow((state) => ({ registerBatch: state.registerBatch }))
  );

  const ids = props.r["library-playlists"];

  useEffect(() => {
    if (ids.length > 0) {
      registerBatch(ids);
      setRegistered(true);
    }
  }, [registerBatch, ids]);

  return (
    <>
      {registered
        ? ids.map((k) => <LibraryPlaylistDrawer key={k} drawerId={k} />)
        : null}
    </>
  );
}
