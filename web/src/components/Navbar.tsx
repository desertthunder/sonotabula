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
    <nav className="flex border-b-4 border-green-500 py-1 pl-4 gap-4 bg-white justify-between items-center">
      <section>
        <Link
          to="/"
          className="text-lg text-black flex items-center hover:text-green-500"
        >
          <i className="i-ri-spotify-line text-xl  mr-1" />
          <span>Dashspot</span>
        </Link>
      </section>

      <section className="flex flex-1 items-center text-2xl justify-end">
        <Link to="/profile" className="flex items-center text-3xl group">
          <i className="i-ri-account-circle-2-fill text-green-500 group-hover:text-green-400 group-hover:scale-110 transition-all duration-300" />
        </Link>
        {/* <i className="i-ri-notification-2-fill text-gray-400" /> */}
      </section>
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
