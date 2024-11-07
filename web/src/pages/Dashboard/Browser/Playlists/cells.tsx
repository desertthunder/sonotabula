import { useCallback, useEffect, useState } from "react";
import {
  useTransitionStyles,
  useFloating,
  useClick,
  useInteractions,
  useDismiss,
} from "@floating-ui/react";
import { usePlaylistAction } from "@/libs/hooks/mutations";

export function PlaylistActionsCell(props: { playlistID: string }) {
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const syncMutation = usePlaylistAction(props.playlistID, "sync");
  const analyzeMutation = usePlaylistAction(props.playlistID, "analyze");

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
    syncMutation.mutate();
    setIsOpen(false);
  }, [syncMutation]);

  const analyzeHandler = useCallback(() => {
    analyzeMutation.mutate();
    setIsOpen(false);
  }, [analyzeMutation]);

  useEffect(() => {
    if (syncMutation.isPending || analyzeMutation.isPending) {
      setIsLoading(true);

      return;
    }

    const timeout = setTimeout(() => {
      setIsLoading(false);
    }, 1000);

    return () => clearTimeout(timeout);
  }, [syncMutation.isPending, analyzeMutation.isPending]);

  return (
    <>
      <div ref={refs.setReference} {...getReferenceProps()}>
        <button
          className={[
            isOpen ? "bg-primary text-white" : "bg-white text-primary",
            isOpen ? "border-primary" : "border-zinc-100",
            "flex items-center px-2 py-1 text-sm",
            "shadow rounded",
            "hover:bg-primary hover:text-white hover:border-primary",
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
