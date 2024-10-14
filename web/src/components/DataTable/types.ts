enum Resources {
  Playlist = "Playlist",
}

enum Title {
  Playlist = "Playlist",
  Track = "Track",
}

export type Playlist = {
  id: string;
  spotify_id: string;
  name: string;
  is_synced: boolean;
  is_analyzed: boolean;
  description?: string;
  owner_id?: string;
  version?: string;
  image_url?: string;
  public?: boolean;
  shared?: boolean;
};

type Resource<T extends Resources> = T extends Resources.Playlist
  ? Playlist
  : never;

type Column<T extends Resources> = {
  title: string;
  field: keyof Resource<T>;
};

type TableDefinition<T extends Resources> = {
  title: Title;
  columns: Column<T>[];
  data: Resource<T>[];
};

function getPlaylistDefinition(
  data: Resource<Resources.Playlist>[]
): TableDefinition<Resources.Playlist> {
  return {
    title: Title.Playlist,
    columns: [
      { title: "Cover", field: "image_url" },
      { title: "Name", field: "name" },
      { title: "Synced", field: "is_synced" },
      { title: "Analyzed", field: "is_analyzed" },
      { title: "Description", field: "description" },
      { title: "Owner ID", field: "owner_id" },
      { title: "Version", field: "version" },
      { title: "Public", field: "public" },
      { title: "Shared", field: "shared" },
    ] as Column<Resources.Playlist>[],
    data,
  };
}

export function useTable<T extends Resources>(
  data: Resource<T>[],
  type: string
): TableDefinition<T> {
  switch (type) {
    case Resources.Playlist:
      return getPlaylistDefinition(
        data as Resource<Resources.Playlist>[]
      ) as TableDefinition<T>;
    default:
      throw new Error("Invalid type");
  }
}
