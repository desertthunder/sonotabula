/**
 * Playlists Dashboard Browser Page
 */

import { Table } from "./table";

export function PlaylistsBrowser() {
  return (
    <div className="flex flex-col w-full text-sm min-h-min">
      <section data-testid="search-bar" className="p-4 bg-white">
        <i className="i-ri-search-line" />
      </section>
      <header className="flex flex-col justify-between p-4 bg-white border-y">
        <p className="text-gray-500">Breadcrumbs</p>
        <h1 className="text-2xl font-medium">Playlists Browser</h1>
      </header>
      <div className="md:grid md:grid-cols-2 lg:grid-cols-4 divide-x">
        <article className="p-4 bg-white border-r border-b">
          <h2 className="text-lg">Card 1</h2>
          <p>Card 1 Content</p>
        </article>
        <article className="p-4 bg-white border-r border-b">
          <h2 className="text-lg">Card 2</h2>
          <p>Card 2 Content</p>
        </article>
        <article className="p-4 bg-white border-r border-b">
          <h2 className="text-lg">Card 3</h2>
          <p>Card 3 Content</p>
        </article>
        <article className="p-4 bg-white border-b">
          <h2 className="text-lg">Card 4</h2>
          <p>Card 4 Content</p>
        </article>
      </div>
      <section className="bg-emerald-500 py-8 px-4 text-zinc-50 border-y">
        <h2 className="text-lg">Section Title</h2>
        <p>Section Content</p>
      </section>
      <section className="p-4 bg-emerald-500 text-zinc-50">
        <h2 className="text-lg">Form Filters</h2>
        <p>Form Content</p>
      </section>
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
      <footer className="p-4 bg-white border-y" data-testid="pagination">
        <h2 className="text-lg">Pagination</h2>
        <p>Pagination Content</p>
      </footer>
    </div>
  );
}
