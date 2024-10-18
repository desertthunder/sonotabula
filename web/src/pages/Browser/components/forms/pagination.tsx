export function PaginationForm({
  pageSize,
  setPageSize,
  sortBy,
  setSortBy,
}: {
  pageSize: number;
  setPageSize: (pageSize: number) => void;
  sortBy: string | undefined;
  setSortBy: (sortBy: string | undefined) => void;
}) {
  return (
    <form className="flex gap-2 bg-slate-200 p-4 text-sm mb-12">
      <div className="flex flex-1 items-center justify-center">
        <input
          type="search"
          placeholder="Search by song title, artist, or album..."
          className="rounded-l-md p-2 flex-1"
        />
        <button className="bg-slate-100 p-2 rounded-r-md">Search</button>
      </div>
      <div className="flex gap-0 rounded-md p-4">
        <label className="bg-slate-100 p-2 rounded-l-md">Items per page:</label>
        <select
          className="rounded-r-md"
          value={parseInt(pageSize.toString())}
          onChange={(e) => setPageSize(Number(e.target.value))}
        >
          {[5, 10, 25, 50, 100].map((size) => (
            <option key={size} value={size} disabled={size === pageSize}>
              {size}
            </option>
          ))}
        </select>
      </div>
      <div className="flex gap-0 rounded-md p-4">
        <label className="p-2 rounded-l-md bg-slate-100">Sort by:</label>
        <select
          className="rounded-r-md"
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
        >
          <option value="">None</option>
          <option value="name">Name</option>
          <option value="num_tracks">Tracks</option>
        </select>
      </div>
    </form>
  );
}

export const PagerButton = ({
  label,
  disabled,
  onClick,
}: {
  label: string;
  disabled?: boolean;
  onClick: () => void;
}) => (
  <button
    className={[
      "flex gap-2 items-center",
      "border border-slate-300",
      "rounded-md",
      "py-1",
      label.includes("Prev") ? "pr-2" : "pl-2",
      "bg-slate-100",
      disabled
        ? "cursor-not-allowed bg-slate-200 text-slate-500"
        : "cursor-pointer hover:bg-slate-200",
    ].join(" ")}
    onClick={onClick}
    disabled={disabled}
  >
    {label.includes("Prev") ? (
      <i className="i-ri-arrow-left-s-line text-lg font-semibold" />
    ) : null}
    <span className="text-xs">{label}</span>
    {label.includes("Next") ? (
      <i className="i-ri-arrow-right-s-line text-lg font-semibold" />
    ) : null}
  </button>
);

export function Pager({
  page,
  setPage,
  totalPages,
}: {
  page: number;
  setPage: (page: number) => void;
  totalPages?: number;
}) {
  return (
    <div className="flex gap-4 m-4">
      <PagerButton
        label="Prev"
        disabled={page === 1}
        onClick={() => setPage(Math.max(1, page - 1))}
      />
      <span className={["flex gap-2 items-center", "", "text-xs"].join(" ")}>
        Page {page}
        {totalPages ? ` of ${totalPages}` : null}
      </span>
      <PagerButton
        label="Next"
        disabled={totalPages ? page === totalPages : true}
        onClick={() => setPage(Math.min(totalPages ? totalPages : 1, page + 1))}
      />
    </div>
  );
}
