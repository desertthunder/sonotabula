import { usePlaylistFilters } from "./store";
import { Pager } from "@/pages/Dashboard/components/pagination";

export function BrowserPlaylistPagination() {
  const page = usePlaylistFilters((state) => state.page);
  const total = usePlaylistFilters((state) => state.total);
  const pageSize = usePlaylistFilters((state) => state.pageSize);
  const setPage = usePlaylistFilters((state) => state.setPage);
  const isLoading = usePlaylistFilters((state) => state.isFetching);
  return (
    <footer className="bg-white border-y" data-testid="pagination">
      <Pager
        page={page}
        setPage={setPage}
        totalPages={Math.ceil(total / pageSize)}
        showNumbers
        isLoading={isLoading}
      />
    </footer>
  );
}
