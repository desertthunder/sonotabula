import { Outlet } from "react-router-dom";
import React from "react";
import type { BrowserContext } from "./context";

export function BrowserLayout() {
  const [title, setTitle] = React.useState("Browser");
  const [description, setDescription] = React.useState("View synced data");

  React.useEffect(() => {
    if (title === "Browser") {
      document.title = "Browser";
    } else {
      document.title = `${title} - Browser`;
    }
  }, [title]);

  return (
    <div className="flex flex-1 gap-8 p-8 justify-between text-sm">
      <section className="flex flex-col gap-4 flex-1">
        <h1 className="font-medium text-base">{title}</h1>
        <h2>{description}</h2>
        <div className="rounded-lg bg-slate-50 p-8 drop-shadow-lg">
          <div className="overflow-y-auto flex-1 max-h-[450px] ">
            <Outlet
              context={
                {
                  setTitle,
                  setDescription,
                } satisfies BrowserContext
              }
            />
          </div>
        </div>
      </section>
    </div>
  );
}
