import { useQuery } from "@tanstack/react-query";
import { useTokenStore } from "@/store";
import { Breadcrumbs, BrowserCard } from "@/components/common";
import { useSavedCounts } from "@/libs/hooks";
import { BrowserAlbumListResponse } from "@/libs/types/api";
import { Table } from "./table";
async function fetchBrowserAlbumMetadata(token: string | null) {
  if (!token) {
    throw new Error("No token");
  }

  const url = new URL(
    "/server/api/v1/browser/albums/meta",
    window.location.origin
  );
  const response = await fetch(url.toString(), {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch album metadata");
  }

  return await response.json();
}

function useBrowserAlbumMetadata() {
  const token = useTokenStore((state) => state.token);
  const query = useQuery({
    queryKey: ["browser", "albums", "metadata"],
    queryFn: () => fetchBrowserAlbumMetadata(token),
  });

  return query;
}

async function fetchBrowserAlbums(token: string | null) {
  if (!token) {
    throw new Error("No token");
  }

  const url = new URL("/server/api/v1/browser/albums", window.location.origin);
  const response = await fetch(url.toString(), {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch albums");
  }

  return (await response.json()) as BrowserAlbumListResponse;
}

function useBrowserAlbums() {
  const token = useTokenStore((state) => state.token);
  const query = useQuery({
    queryKey: ["browser", "albums"],
    queryFn: () => fetchBrowserAlbums(token),
  });

  return query;
}

function AlbumBrowserCards({
  metadata,
  counts,
}: {
  metadata: any;
  counts: any;
}) {
  return (
    <section className="md:grid md:grid-cols-2 lg:grid-cols-4 divide-x">
      <BrowserCard
        title="Albums"
        helpText="The number of albums saved in your spotify library."
      >
        {counts.isLoading ? (
          <i className="i-ri-loader-line animate-spin" />
        ) : counts.isError ? (
          <span className="text-error font-medium">Something went wrong</span>
        ) : counts.data ? (
          <span className="text-primary font-medium">{counts.data.albums}</span>
        ) : null}
      </BrowserCard>
      <BrowserCard
        title="Synced Albums"
        helpText="The number of albums synced with your spotify account."
      >
        {metadata.isLoading ? (
          <i className="i-ri-loader-line animate-spin" />
        ) : metadata.isError ? (
          <span className="text-error font-medium">Something went wrong</span>
        ) : metadata.data ? (
          <span className="text-primary font-medium">
            {metadata.data.total_synced}
          </span>
        ) : null}
      </BrowserCard>
      <BrowserCard
        title="Analyzed Albums"
        helpText="The number of albums analyzed."
      >
        {metadata.isLoading ? (
          <i className="i-ri-loader-line animate-spin" />
        ) : metadata.isError ? (
          <span className="text-error font-medium">Something went wrong</span>
        ) : metadata.data ? (
          <span className="text-primary font-medium">
            {metadata.data.total_analyzed}
          </span>
        ) : null}
      </BrowserCard>
      <BrowserCard
        title="Total Tracks"
        helpText="The number of tracks in your synced albums."
      >
        {metadata.isLoading ? (
          <i className="i-ri-loader-line animate-spin" />
        ) : metadata.isError ? (
          <span className="text-error font-medium">Something went wrong</span>
        ) : metadata.data ? (
          <span className="text-primary font-medium">
            {metadata.data.total_tracks}
          </span>
        ) : null}
      </BrowserCard>
    </section>
  );
}

export function AlbumsBrowser() {
  const query = useBrowserAlbums();
  const metaQuery = useBrowserAlbumMetadata();
  const counts = useSavedCounts();

  if (query.isLoading || metaQuery.isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="flex flex-col w-full text-sm min-h-min">
      <Breadcrumbs context="albums" />
      <AlbumBrowserCards metadata={metaQuery} counts={counts} />
      <main className="bg-white flex flex-col flex-1 overflow-auto">
        <header className="p-4 flex items-center justify-between border-y border-t-primary">
          <h2 className="text-lg">Table</h2>
        </header>
        <Table context={query} />
      </main>
    </div>
  );
}
