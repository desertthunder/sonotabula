import React, { useEffect, useState } from "react";
import { useBrowserPlaylists } from "@libs/hooks";
import { useQueryClient } from "@tanstack/react-query";
import { PlaylistTable } from "./components/tables/playlists";
import { PaginationForm, Pager } from "./components/forms/pagination";
import { FilterForm } from "./components/forms/filters";

export function PlaylistsPage(props: { children: React.ReactNode }) {
  // TODO: Move to a store.
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState<number>();
  const [pageSize, setPageSize] = useState(10);
  const [sortBy, setSortBy] = useState<string | undefined>();
  const [filters] = useState<string[][] | undefined>();

  const client = useQueryClient();
  const query = useBrowserPlaylists({ page, pageSize, filters }, client);

  useEffect(() => {
    if (query.data?.pagination) {
      setTotalPages(query.data.pagination.num_pages);
    }
  }, [query.data?.pagination, props]);

  useEffect(() => {
    if (pageSize) {
      client.invalidateQueries({
        predicate: (query) => {
          return query.queryKey[0] === "browser-playlists";
        },
      });
    }

    if (page) {
      client.invalidateQueries({
        queryKey: ["browser-playlists", page - 1],
      });
    }
  }, [page, pageSize, client]);

  return (
    <>
      {props.children}
      <div className="rounded-lg bg-slate-50 p-8 drop-shadow-lg">
        <h2 className="text-lg font-bold">Playlists</h2>
        <FilterForm updateFilters={(filters) => console.log(filters)} />
        <PaginationForm
          pageSize={pageSize}
          setPageSize={setPageSize}
          sortBy={sortBy}
          setSortBy={setSortBy}
        />
        <div className="overflow-y-auto flex-1 max-h-[450px]">
          {query.isLoading ? <div>Loading...</div> : null}
          {query.isFetching ? <div>Fetching...</div> : null}
          {query.isError ? (
            <div>Error: {query.error.message}</div>
          ) : (
            <PlaylistTable
              data={query.data?.data || []}
              page={page}
              pageSize={pageSize}
              setTotalPages={setTotalPages}
              sortBy={sortBy}
              filters={filters}
            />
          )}
        </div>
        <Pager page={page} setPage={setPage} totalPages={totalPages} />
      </div>
    </>
  );
}
