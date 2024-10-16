import React from "react";

export function BrowserLayout(props: { children: React.ReactNode }) {
  return (
    <div className="flex flex-1 gap-8 p-8 justify-between text-sm">
      <section className="flex flex-col gap-4 flex-1">
        <h1 className="font-medium text-base">Browser</h1>
        <h2>View your synced data</h2>
        <div className="rounded-lg bg-slate-50 p-8 drop-shadow-lg">
          <div className="overflow-y-auto flex-1 max-h-[450px] ">
            {props.children}
          </div>
        </div>
      </section>
    </div>
  );
}
