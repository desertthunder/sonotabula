import { useFetch } from "@/libs/hooks";
import { useMemo } from "react";
import type { Artist, Playlist, Album, Track } from "@/libs/types";
import { ResourceKey } from "@/libs/types";
import { decodeUnicode } from "@/libs/helpers";

interface Props {
  scope: ResourceKey;
}

type TableHeaders = Record<ResourceKey, string[]>;

type AccessedType<T extends ResourceKey> = T extends ResourceKey.LibraryAlbums
  ? Album
  : T extends ResourceKey.LibraryArtists
  ? Artist
  : T extends ResourceKey.LibraryPlaylists
  ? Playlist
  : T extends ResourceKey.LibraryTracks
  ? Track
  : never;

const tableHeaders: TableHeaders = {
  [ResourceKey.LibraryPlaylists]: [
    "Data",
    "Name",
    "Description",
    "Size",
    "Link",
  ],

  [ResourceKey.LibraryAlbums]: [
    "Data",
    "Name",
    "Description",
    "Artist",
    "#",
    "Year",
  ],
  [ResourceKey.LibraryTracks]: [
    "Data",
    "Name",
    "Artist",
    "Album",
    "Duration",
    "Link",
  ],
  [ResourceKey.LibraryArtists]: ["Data", "Name", "Genres", "Link"],
};

function translateHeader(header: string): string {
  switch (header) {
    case "Data":
      return "image_url";
    case "#":
      return "total_tracks";
    case "Size":
      return "num_tracks";
    case "Year":
      return "release_date";
    case "Artist":
      return "artist_name";
    case "Duration":
      return "duration_ms";
    case "Album":
      return "album_name";
    default:
      return header.toLowerCase();
  }
}

function tableProps<T extends ResourceKey>(
  scope: ResourceKey
): {
  headers: string[];
  accessors: (keyof AccessedType<T>)[];
} {
  const headers = tableHeaders[scope].map((header) => {
    if (scope === ResourceKey.LibraryPlaylists && header === "Size") {
      return "#";
    }

    return header;
  });

  return {
    headers,
    accessors: tableHeaders[scope].map((header) => {
      return translateHeader(header) as keyof AccessedType<T>;
    }),
  };
}

function Cell({
  accessor,
  value,
}: {
  accessor: string | string[];
  value: string;
}) {
  switch (accessor) {
    case "image_url":
      return (
        <td className="text-center w-16">
          <img src={value} alt="album" className="w-full" />
        </td>
      );
    case "release_date":
      return <td>{value.split("-")[0]}</td>;
    case "description":
      return (
        <td>
          <em>{value ? decodeUnicode(value) : "None"}</em>
        </td>
      );
    case "link":
      return (
        <td>
          <a
            className="hover:text-green-500 i-ri-external-link-line"
            href={value}
            target="_blank"
            rel="noreferrer"
          >
            {value}
          </a>
        </td>
      );
    case "num_tracks":
    case "total_tracks":
      return <td className="text-center">{value}</td>;
    case "genres":
      return <td>{Array.isArray(value) ? value.join(", ") : value}</td>;
    default:
      return <td>{value}</td>;
  }
}

export function LibraryTable({ scope }: Props) {
  const context = useFetch<typeof scope>(scope, 10);

  const { headers, accessors } = useMemo(() => {
    return tableProps(scope);
  }, [scope]);

  if (context.isError) {
    return <div>Error: {context.error.message}</div>;
  }

  return (
    <table className="table-auto w-full py-0 my-0 overflow-scroll h-full text-xs text-left text-gray-800 ">
      <thead className="sticky top-0">
        <tr>
          {headers.map((header) => (
            <th key={header}>{header !== "Data" ? header : ""}</th>
          ))}
        </tr>
      </thead>
      {context.isLoading ? (
        <tbody>
          <tr>
            <td>Loading...</td>
          </tr>
        </tbody>
      ) : (
        context.data && (
          <tbody>
            {context.data.map((item) => (
              <tr key={item.spotify_id}>
                {accessors.map((accessor) => (
                  <Cell
                    key={accessor}
                    accessor={accessor}
                    value={item[accessor]}
                  />
                ))}
              </tr>
            ))}
          </tbody>
        )
      )}
    </table>
  );
}
