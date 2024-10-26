import { Link } from "wouter";
import { LastPlayed } from "./LastPlayed";
import { useCallback } from "react";
import { useListeningHistory } from "@libs/hooks";

export function Navbar() {
  const query = useListeningHistory();

  const refreshHandler = useCallback(() => {
    query.refetch();
  }, [query]);

  return (
    <nav className="flex border-b-4 border-green-500 py-1 pl-4 bg-white justify-between">
      <Link
        to="/"
        className="text-lg text-black flex items-center hover:text-green-500"
      >
        <i className="i-ri-spotify-line text-xl  mr-1" />
        <span>Dashspot</span>
      </Link>
      <section className="flex-shrink">
        {query.isPending ? (
          <i className="i-ri-loader-line animate-spin" />
        ) : null}
        {query.isError ? (
          <span className="text-red-500">
            {query.error?.code >= 500
              ? "Something Went Wrong"
              : query.error?.message}
          </span>
        ) : null}
        {query.isSuccess ? (
          <LastPlayed
            data={query.data}
            refresh={refreshHandler}
            isFetching={query.isFetching}
          />
        ) : null}
      </section>
    </nav>
  );
}
