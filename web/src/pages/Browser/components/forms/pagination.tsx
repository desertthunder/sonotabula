import toInteger from "lodash/toInteger";
import { useCallback, useMemo } from "react";

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
  className,
}: {
  label: string;
  disabled?: boolean;
  onClick: () => void;
  className?: string;
}) => (
  <button
    className={[
      "flex gap-2 items-center",
      "py-2 px-4 font-semibold text-sm",
      "bg-zinc-50 hover:bg-green-400",
      disabled
        ? "pointer-events-none bg-slate-200 text-slate-500"
        : "cursor-pointer",
      className,
    ].join(" ")}
    onClick={onClick}
    disabled={disabled}
  >
    {label.includes("Prev") ? (
      <i className="i-ri-arrow-left-s-line text-lg font-semibold" />
    ) : null}
    <span>{label}</span>
    {label.includes("Next") ? (
      <i className="i-ri-arrow-right-s-line text-lg font-semibold" />
    ) : null}
  </button>
);

interface PagerProps {
  page: number;
  setPage: (page: number) => void;
  totalPages?: number;
  showNumbers: boolean;
  isLoading: boolean;
}

export function Pager(props: PagerProps) {
  const labels = useMemo(() => {
    if (!props.totalPages) {
      return [];
    }

    const pages = Array.from({ length: props.totalPages }, (_, i) => i + 1);
    const first = pages[0];
    const last = pages[pages.length - 1];

    if (props.totalPages < 10) {
      return pages;
    }

    if (props.page < 5) {
      return [...pages.slice(0, 5), "...", last];
    }

    if (props.page > props.totalPages - 5) {
      return [first, "...", ...pages.slice(-5)];
    }

    return [
      first,
      "...",
      ...pages.slice(props.page - 2, props.page + 1),
      "...",
      last,
    ];
  }, [props.page, props.totalPages]);

  const nextHandler = useCallback(() => {
    if (!props.totalPages) {
      return;
    }

    props.setPage(Math.min(props.totalPages, props.page + 1));
  }, [props]);

  const prevHandler = useCallback(() => {
    props.setPage(Math.max(1, props.page - 1));
  }, [props]);

  const numberedHandler = useCallback(
    (page: string | number) => {
      props.setPage(toInteger(page));
    },
    [props]
  );

  return (
    <div className="mt-4 py-4 border-t-2 flex items-center justify-center">
      <PagerButton
        label="Prev"
        disabled={props.page === 1 || props.isLoading}
        onClick={prevHandler}
        className="border-x rounded-l  border-slate-400 border-y"
      />
      {props.showNumbers
        ? labels.map((label, i) => {
            if (label === "...") {
              return (
                <button
                  disabled
                  key={i}
                  className="items-center py-2 px-6 font-bold text-sm border-y border-r border-slate-400"
                >
                  ...
                </button>
              );
            }

            return (
              <PagerButton
                key={i}
                label={label.toString()}
                disabled={props.page === label || props.isLoading}
                onClick={() => numberedHandler(label)}
                className="items-center py-2 border-y border-r border-slate-400"
              />
            );
          })
        : null}
      <PagerButton
        label="Next"
        disabled={props.page === props.totalPages || props.isLoading}
        onClick={nextHandler}
        className="border-r border-y border-slate-400 rounded-r"
      />
    </div>
  );
}
