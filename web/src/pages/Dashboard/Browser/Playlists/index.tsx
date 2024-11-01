/**
 * Playlists Dashboard Browser Page
 */

import React from "react";
import { FilterForm } from "./filters/form";
import { BrowserPlaylistPagination } from "./filters/pagination";
import { Table } from "./table";
import { Link } from "wouter";
interface BrowserCardProps {
  title: string;
  helpText: string;
  content?: string;
  children?: React.ReactNode;
}

function Breadcrumbs() {
  const Links = [
    { label: "Home", href: "/", disabled: false },
    { label: "Dashboard", href: "/dashboard", disabled: false },
    {
      label: "Playlists",
      href: "/dashboard/browser/playlists",
      disabled: true,
    },
  ];
  return (
    <header className="flex flex-col justify-between p-4 bg-white border-t">
      <p className="text-gray-500 flex items-center">
        {Links.map((link, index) => (
          <React.Fragment key={index}>
            <Link
              href={link.href}
              className={
                link.disabled ? "pointer-events-none" : "hover:text-emerald-500"
              }
            >
              <span className="group-hover:text-emerald-500">{link.label}</span>
            </Link>
            {index < Links.length - 1 && (
              <i className="i-ri-arrow-right-s-line align-middle" />
            )}
          </React.Fragment>
        ))}
      </p>
      <h1 className="text-2xl font-medium">Playlists Browser</h1>
    </header>
  );
}

export function BrowserCard({
  title,
  helpText,
  content,
  children,
}: BrowserCardProps) {
  return (
    <article className="bg-white border-t border-emerald-500 flex flex-col gap-2">
      <header className="text-lg p-4 pb-2">{title}</header>
      <section className="p-4 border-y">
        {content ? (
          content
        ) : children ? (
          children
        ) : (
          <p className="text-gray-500">No content</p>
        )}
      </section>
      <footer className="text-xs text-gray-500 p-4">{helpText}</footer>
    </article>
  );
}

export function PlaylistsBrowser() {
  return (
    <div className="flex flex-col w-full text-sm min-h-min">
      <section data-testid="search-bar" className="p-4 bg-white">
        <i className="i-ri-search-line" />
      </section>
      <Breadcrumbs />
      <section className="md:grid md:grid-cols-2 lg:grid-cols-4 divide-x">
        <BrowserCard
          title="Total Playlists"
          helpText="The number of playlists saved in your spotify library."
          content="Card 1 Content"
        />
        <BrowserCard
          title="Synced Playlists"
          helpText="The number of playlists synced with your spotify account."
        />
        <BrowserCard
          title="Analyzed"
          helpText="The number of playlists analyzed for recommendations."
        />
        <BrowserCard title="Card 4" helpText="Card 4 Help Text" />
      </section>
      <FilterForm />
      <main
        data-testid="table"
        className="bg-white flex flex-col flex-1 overflow-auto"
      >
        <header className="p-4">
          <h2 className="text-lg">Table</h2>
          <p>Table Content</p>
        </header>
        <section className="overflow-auto">
          <Table />
        </section>
      </main>
      <BrowserPlaylistPagination />
    </div>
  );
}
