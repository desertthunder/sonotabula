import { Tabs } from "./Tabs";
import { useFetch, ResourceKey } from "@/libs/hooks";
import { decodeUnicode } from "@/libs/helpers";
import React from "react";

const defaultKey = ResourceKey.LibraryPlaylists;

export function LibraryCard() {
  const tab = React.useState(defaultKey);
  const query = useFetch<typeof defaultKey>(defaultKey, 15);

  if (query.isLoading) {
    return <div>Loading...</div>;
  }

  if (query.isError) {
    return <div>Error: {query.error.message}</div>;
  }
  if (query.data) {
    console.log(query.data);
  }

  return (
    <div className="card h-full">
      <header>
        <h1 className="">Library</h1>
        <h2 className="">I dunno</h2>
      </header>
      <Tabs current={tab} />
      <main>
        <table className="table-auto h-full">
          <thead>
            <tr>
              <th>Data</th>
              <th>Name</th>
              <th>Description</th>
              <th>Size</th>
              <th>Link</th>
            </tr>
          </thead>
          <tbody>
            {query.data
              ? query.data.map((playlist) => {
                  return (
                    <tr key={playlist.spotify_id}>
                      <td>
                        <a
                          href={playlist.link}
                          className="hover:text-green-500 i-ri-bar-chart-box-line"
                        />
                      </td>
                      <td>{playlist.name}</td>
                      <td>
                        {playlist.description ? (
                          decodeUnicode(playlist.description)
                        ) : (
                          <em>Description not set.</em>
                        )}
                      </td>
                      <td>{playlist.num_tracks}</td>
                      <td>
                        <a
                          href={playlist.link}
                          className="text-blue-500 hover:underline"
                        >
                          Link
                        </a>
                      </td>
                    </tr>
                  );
                })
              : null}
          </tbody>
        </table>
      </main>
    </div>
  );
}
