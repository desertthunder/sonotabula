import { useCallback, useEffect, useState } from "react";
import {
  useTransitionStyles,
  useFloating,
  useClick,
  useInteractions,
  useDismiss,
} from "@floating-ui/react";
import { useMutation } from "@tanstack/react-query";
import { useTokenStore } from "@/store";

type TaskArgs = {
  pid: string;
  operation: "sync" | "analyze";
  token: string | null;
};

async function callTask({ pid, operation, token }: TaskArgs) {
  if (!token) {
    throw new Error("No token available");
  }

  const url = new URL(`/api/v1/browser/playlists/${pid}`, window.location.href);

  const res = await fetch(url.toString(), {
    method: "PATCH",
    body: JSON.stringify({ operation }),
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  });

  if (!res.ok) {
    throw new Error(`Failed to ${operation} playlist`);
  }

  return await res.json();
}

export function PlaylistActionsCell(props: { playlistID: string }) {
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const token = useTokenStore((state) => state.token);
  const taskMutation = useMutation({
    mutationFn: callTask,
  });

  const { refs, floatingStyles, context } = useFloating({
    open: isOpen,
    onOpenChange: setIsOpen,
  });
  const { isMounted, styles } = useTransitionStyles(context, {
    duration: 500,
    initial: {
      opacity: 0,
      transform: "scale(1)",
    },
  });
  const click = useClick(context);
  const dismiss = useDismiss(context, { outsidePress: true });

  const { getReferenceProps, getFloatingProps } = useInteractions([
    click,
    dismiss,
  ]);

  const syncHandler = useCallback(() => {
    taskMutation.mutate({ pid: props.playlistID, operation: "sync", token });
    setIsOpen(false);
  }, [props, taskMutation, token]);

  const analyzeHandler = useCallback(() => {
    taskMutation.mutate({ pid: props.playlistID, operation: "analyze", token });
    setIsOpen(false);
  }, [props, taskMutation, token]);

  useEffect(() => {
    if (taskMutation.isPending) {
      setIsLoading(true);

      return;
    }

    const timeout = setTimeout(() => {
      setIsLoading(false);
    }, 1000);

    return () => clearTimeout(timeout);
  }, [taskMutation.isPending]);

  return (
    <>
      <div ref={refs.setReference} {...getReferenceProps()}>
        <button
          className={[
            isOpen ? "bg-emerald-500 text-white" : "bg-white text-emerald-500",
            isOpen ? "border-emerald-500" : "border-zinc-100",
            "flex items-center px-2 py-1 text-sm",
            "shadow rounded",
            "hover:bg-emerald-500 hover:text-white hover:border-emerald-500",
            isLoading ? "cursor-wait pointer-events-none" : "",
          ].join(" ")}
          disabled={isLoading}
        >
          <span className="hidden lg:inline">Actions</span>
          <i
            className={[
              isLoading
                ? "i-ri-loader-2-line animate-spin"
                : "i-ri-arrow-down-s-line",
              "lg:ml-2",
              "duration-500 transition-transform",
              isOpen ? "transform rotate-180" : "",
              "text-center",
            ].join(" ")}
          />
        </button>
      </div>
      {isOpen && (
        <div
          ref={refs.setFloating}
          style={{ ...floatingStyles, zIndex: 10, width: "max-content" }}
          {...getFloatingProps()}
        >
          {isMounted && (
            <div
              style={styles}
              className={[
                "bg-white text-xs md:text-sm",
                "border rounded-md py-1",
                "w-20",
                "flex flex-col items-start divide-y",
              ].join(" ")}
            >
              <button
                className="p-2 bg-white hover:bg-zinc-100 w-full"
                onClick={syncHandler}
              >
                Sync
              </button>
              <button
                className="p-2 bg-white hover:bg-zinc-100 w-full"
                onClick={analyzeHandler}
              >
                Analyze
              </button>
            </div>
          )}
        </div>
      )}
    </>
  );
}
