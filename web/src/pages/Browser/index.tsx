import { Outlet } from "react-router-dom";
import React from "react";
import type { BrowserContext } from "./context";

export function BrowserLayout() {
  const [title, setTitle] = React.useState("Browser");
  const [description, setDescription] = React.useState("View synced data");
  const [pager, setPager] = React.useState<{
    total: number;
    per_page: number;
    page: number;
    count?: number;
  }>();

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
                  title,
                  setTitle,
                  description,
                  setDescription,
                  setPagination: setPager,
                } satisfies BrowserContext
              }
            />
          </div>
          {pager ? (
            <>
              <span className="text-xs text-gray-500">
                Viewing Page {pager.page} of{" "}
                {Math.ceil(pager.total / pager.per_page)}.{" "}
              </span>
              {pager.count && pager.count >= 0 ? (
                <span className="text-xs text-gray-500">
                  Showing {pager.count} of {pager.total}
                </span>
              ) : null}
            </>
          ) : null}
        </div>
      </section>
    </div>
  );
}
