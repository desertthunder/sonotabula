import React from "react";

interface BrowserCardProps {
  title: string;
  helpText: string;
  content?: string;
  children?: React.ReactNode;
}

export function BrowserCard({
  title,
  helpText,
  content,
  children,
}: BrowserCardProps) {
  return (
    <article className="bg-white border-t border-primary flex flex-col gap-2">
      <div className="flex border-y items-end p-4 gap-2">
        <header className="text-lg">{title}</header>
        <section className=" text-2xl font-semibold font-titles">
          {content ? (
            content
          ) : children ? (
            children
          ) : (
            <p className="text-gray-500">No content</p>
          )}
        </section>
      </div>
      <footer className="text-xs text-gray-500 px-4 pb-2 align-middle">
        {helpText}
      </footer>
    </article>
  );
}
