import { useFetch } from "@/libs/hooks";
import { useMemo } from "react";
import type { Artist, Playlist, Album, Track } from "@/libs/types";
import { ResourceKey } from "@/libs/types";
import { decodeUnicode } from "@/libs/helpers";
import { Link, ScrollArea, Table, Text } from "@radix-ui/themes";

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
      return <img src={value} alt="album" className="w-8 h-8" />;
    case "release_date":
      return <Text>{value.split("-")[0]}</Text>;
    case "description":
      return (
        <Text>
          <em>{value ? decodeUnicode(value) : "None"}</em>
        </Text>
      );
    case "link":
      return (
        <Link
          className="hover:text-green-500 text-lg"
          href={value}
          target="_blank"
          rel="noreferrer"
        >
          <i className="i-ri-external-link-line" />
        </Link>
      );
    case "num_tracks":
    case "total_tracks":
      return <Text className="text-center">{value}</Text>;
    case "genres":
      return <Text>{Array.isArray(value) ? value.join(", ") : value}</Text>;
    default:
      return <Text>{value}</Text>;
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

  if (context.isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <ScrollArea
      scrollbars="vertical"
      style={{ minHeight: "400px", height: "500px" }}
    >
      <Table.Root variant="surface" size="2" layout="fixed">
        <Table.Header>
          <Table.Row>
            {headers.map((header) => (
              <Table.ColumnHeaderCell key={header}>
                {header !== "Data" ? header : " "}
              </Table.ColumnHeaderCell>
            ))}
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {context.data?.map((item) => (
            <Table.Row key={item.spotify_id} align="center">
              {accessors.map((accessor, i) =>
                i === 0 ? (
                  <Table.RowHeaderCell key={accessor}>
                    <Cell
                      accessor={accessor}
                      value={item[accessor] as string}
                    />
                  </Table.RowHeaderCell>
                ) : (
                  <Table.Cell key={accessor}>
                    <Cell
                      accessor={accessor}
                      value={item[accessor] as string}
                    />
                  </Table.Cell>
                )
              )}
            </Table.Row>
          ))}
        </Table.Body>
      </Table.Root>
    </ScrollArea>
  );
}
