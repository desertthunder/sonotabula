import React from "react";

export function BrowserLayout(props: { children: React.ReactNode }) {
  return (
    <div className="flex flex-1 gap-8 p-8 justify-between text-sm">
      <section className="flex flex-col gap-4 flex-1">
        <h1 className="font-medium text-base">Browser</h1>
        <h2>View your synced data</h2>
        {props.children}
      </section>
    </div>
  );
}
