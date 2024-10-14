import { useMemo } from "react";
import type { Artist, Playlist, Album, Track } from "@/libs/types";
import { ResourceKey } from "@/libs/types";
import { decodeUnicode } from "@/libs/helpers";

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
      return <img src={value} alt="album" className="w-8 h-8" />;
    case "release_date":
      return <span>{value.split("-")[0]}</span>;
    case "description":
      return (
        <span>
          <em>{value ? decodeUnicode(value) : "None"}</em>
        </span>
      );
    case "link":
      return (
        <a
          className="hover:text-green-500 text-lg"
          href={value}
          target="_blank"
          rel="noreferrer"
        >
          <i className="i-ri-external-link-line" />
        </a>
      );
    case "num_tracks":
    case "total_tracks":
      return <span className="text-center">{value}</span>;
    case "genres":
      return <span>{Array.isArray(value) ? value.join(", ") : value}</span>;
    default:
      return <span>{value}</span>;
  }
}

interface Props<T extends ResourceKey> {
  scope: T;
  data: AccessedType<T>[];
}

export function LibraryTable<T extends ResourceKey>({ scope, data }: Props<T>) {
  const { headers, accessors } = useMemo(() => {
    return tableProps(scope);
  }, [scope]);

  return (
    <div className="overflow-y-auto flex-1 max-h-[600px] rounded-lg">
      <table className="text-sm w-full">
        <thead className="rounded-md">
          <tr className="border-b bg-white">
            {headers.map((header) => (
              <th
                key={header}
                className={[
                  "h-10 px-2 text-left align-middle font-medium text-slate-800",
                ].join(" ")}
              >
                {header !== "Data" ? header : " "}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="last:border-b-0">
          {data?.map((item) => (
            <tr
              key={item.spotify_id}
              className={[
                "border-b transition-colors",
                "bg-white",
                "even:bg-slate-100",
              ].join(" ")}
            >
              {accessors.map((accessor) => (
                <td key={accessor} className={["p-2 align-middle"].join(" ")}>
                  <Cell
                    key={accessor}
                    accessor={accessor}
                    value={item[accessor] as string}
                  />
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
