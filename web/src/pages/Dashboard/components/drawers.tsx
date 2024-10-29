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
      const [, id] = queryKey;
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
        className={`fixed right-0 top-0 bottom-0 w-96 bg-white p-4 shadow-lg transition-transform transform ${
          meta.isOpen ? "translate-x-0" : "translate-x-full"
        }`}
      >
        <button className="text-gray-600 hover:text-gray-800" onClick={toggle}>
          Close
        </button>
        <div className="mt-4">
          {query.isLoading ? "Loading" : null}
          {query.isError ? "Error" : null}
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
