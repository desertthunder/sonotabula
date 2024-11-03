import { useNotifications, WSMessage } from "@/libs/hooks/ws";
import { useListeningHistory } from "@libs/hooks";
import _ from "lodash";
import { useCallback, useEffect, useState } from "react";
import { Link } from "wouter";
import { LastPlayed } from "./LastPlayed";

function StartToast() {
  return (
    <div className="text-sm font-normal flex items-center text-bold">
      <i className="i-ri-notification-2-fill text-amber-400">
        <span className="sr-only">Notification icon</span>
      </i>
      <span className="ms-3">Started Task</span>
    </div>
  );
}

function CompleteToast(props: { handleClick: () => void }) {
  return (
    <div className="text-sm font-normal flex items-center text-bold">
      <i className="i-ri-notification-2-fill text-green-400">
        <span className="sr-only">Notification icon</span>
      </i>
      <span className="ms-3">Task Completed</span>
      <div className="flex-1 flex items-center justify-end">
        <button
          className="text-red-400 hover:text-red-500"
          onClick={props.handleClick}
        >
          <i className="i-ri-close-line" />
        </button>
      </div>
    </div>
  );
}

export function Toaster() {
  const { query, client } = useNotifications();

  const [showToast, setShowToast] = useState(false);
  const [data, setData] = useState<WSMessage | null>(null);

  useEffect(() => {
    if (query.isSuccess && query.data) {
      setShowToast(true);
      const id = _.last(query.data);

      const message = client.getQueryData(["notifications", id]) as WSMessage;

      setData(message);
    }
  }, [query.isSuccess, query.data, client]);

  useEffect(() => {
    if (!showToast) {
      return;
    }

    const timer = setTimeout(() => {
      setShowToast(false);
    }, 3000);

    return () => {
      clearTimeout(timer);
    };
  }, [showToast]);

  useEffect(() => {
    const timer = setTimeout(() => {
      setShowToast(true);
    }, 3000);

    return () => {
      clearTimeout(timer);
    };
  }, []);

  return (
    <div
      id="toast-bottom-right"
      className={[
        "fixed flex items-center w-full max-w-xs",
        "p-4 space-x-4 divide-x rtl:divide-x-reverse rounded-lg shadow right-5 bottom-5 text-gray-400 divide-gray-700 bg-gray-800",
        showToast ? "scale-100" : "scale-0",
        "transition-transform duration-300",
      ].join(" ")}
      role="alert"
    >
      {showToast ? (
        <>
          {data?.type === "task_started" ? (
            <StartToast />
          ) : (
            <CompleteToast
              handleClick={() => {
                setShowToast(false);
              }}
            />
          )}
        </>
      ) : null}
    </div>
  );
}

export function Navbar() {
  const query = useListeningHistory();

  const refreshHandler = useCallback(() => {
    query.refetch();
  }, [query]);

  return (
    <>
      <Toaster />
      <nav className="flex border-b-4 border-green-500 py-1 pl-4 gap-4 bg-white justify-between items-center">
        <section>
          <Link
            to="/"
            className="text-xl font-headings font-medium text-black flex items-center hover:text-green-500 group"
          >
            <i className="i-ri-spotify-line group-hover:i-ri-spotify-fill text-xl  mr-1" />
            <span>Dashspot</span>
          </Link>
        </section>

        <section className="flex flex-1 items-center text-2xl justify-end">
          <Link to="/profile" className="flex items-center text-3xl group">
            <i className="i-ri-account-circle-2-fill text-green-500 group-hover:text-green-400 group-hover:scale-110 transition-all duration-300" />
          </Link>
          <i className="i-ri-notification-2-fill text-gray-400" />
        </section>
        <section className="flex-shrink px-2">
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
    </>
  );
}
