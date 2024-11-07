import { usePlaylistFilters } from "@/store/filters";
import { Pager } from "@/pages/Dashboard/components/pagination";
import { useQueryParams } from "@/libs/hooks/params";
import { useLocation } from "wouter";
import { useCallback, useMemo } from "react";

export function BrowserPlaylistPagination() {
  const [, setLocation] = useLocation();
  const total = usePlaylistFilters((state) => state.total);
  const isLoading = usePlaylistFilters((state) => state.isFetching);
  const params = useQueryParams();
  const pageSize = useMemo(() => {
    return params.get("page_size")
      ? parseInt(params.get("page_size") as string)
      : params.get("pageSize")
      ? parseInt(params.get("pageSize") as string)
      : params.get("per_page")
      ? parseInt(params.get("per_page") as string)
      : 10;
  }, [params]);

  const setPage = useCallback(
    (page: number) => {
      params.set("page", page.toString());
      setLocation(`/dashboard/browser/playlists?${params.toString()}`);
    },
    [setLocation, params]
  );

  return (
    <footer className="bg-white border-y" data-testid="pagination">
      <Pager
        page={params.get("page") ? parseInt(params.get("page") as string) : 1}
        setPage={setPage}
        totalPages={Math.ceil(total / pageSize)}
        showNumbers
        isLoading={isLoading}
      />
    </footer>
  );
}
