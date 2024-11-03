import { useState } from "react";
import {
  useTransitionStyles,
  useFloating,
  useClick,
  useInteractions,
  useDismiss,
} from "@floating-ui/react";

export function Menu() {
  const [isOpen, setIsOpen] = useState(false);

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
          ].join(" ")}
        >
          <span className="hidden lg:inline">Actions</span>
          <i
            className={[
              "i-ri-arrow-down-s-line lg:ml-2",
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
              <button className="p-2 bg-white hover:bg-zinc-100 w-full">
                Sync
              </button>
              <button className="p-2 bg-white hover:bg-zinc-100 w-full">
                Analyze
              </button>
            </div>
          )}
        </div>
      )}
    </>
  );
}
