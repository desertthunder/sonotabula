/**
 * @description User profile page
 */
import { useProfileQuery } from "@/libs/hooks";
import { useMemo } from "react";

function DTitle({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <dt className="md:col-span-1 font-semibold font-headings flex items-center gap-1 py-3 border-b md:last-of-type:border-none">
      {className ? (
        <i className={`text-emerald-600 text-base ${className}`} />
      ) : null}
      <span>{children}</span>
    </dt>
  );
}

function DDetail({ children }: { children: React.ReactNode }) {
  return (
    <dd className="md:col-span-2 font-medium py-3 border-b md:last-of-type:border-none">
      {children}
    </dd>
  );
}

function DescriptionList({ children }: { children: React.ReactNode }) {
  return (
    <dl className="grid grid-cols-1 md:grid-cols-3 gap-y-2 text-sm font-sans md:first-of-type:border-b-2 p-4 md:py-8">
      {children}
    </dl>
  );
}

export function Profile() {
  const query = useProfileQuery();
  const profile = useMemo(() => query.data?.data, [query.data]);

  return (
    <main className="flex flex-col gap-4 p-8 w-full md:w-1/2 md:mx-auto">
      {query.isLoading ? <div>Loading...</div> : null}
      {query.isError ? (
        <div>Error: {query.error.message}</div>
      ) : query.data && profile ? (
        <article className="flex flex-col gap-4 bg-white rounded-md shadow-lg border p-8">
          <header className="flex items-center gap-4 font-headings">
            <div className="relative z-0 group">
              <img
                src={profile.image_url}
                alt="Profile"
                className="rounded-full w-20 h-20 group-hover:opacity-0 transition-opacity duration-300"
              />
              <i className="i-ri-spotify-fill text-emerald-400 w-20 h-20 absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
            </div>
            <h1 className="text-3xl font-semibold flex-1">
              {profile.display_name}
            </h1>
          </header>
          <section>
            <DescriptionList>
              <DTitle className="i-ri-id-card-fill">App ID</DTitle>
              <DDetail>{profile.id}</DDetail>
              <DTitle className="i-ri-spotify-fill">Spotify ID</DTitle>
              <DDetail>{profile.spotify_id}</DDetail>
              <DTitle className="i-ri-ie-fill">Link</DTitle>
              <DDetail>
                <a
                  href={`https://open.spotify.com/user/${profile.spotify_id}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-green-500 flex items-center gap-1"
                >
                  <span>Open</span>
                  <i className="i-ri-external-link-fill" />
                </a>
              </DDetail>
              <DTitle className="i-ri-mail-fill">Email</DTitle>
              <DDetail>{profile.email}</DDetail>
            </DescriptionList>
            <DescriptionList>
              <DTitle className="i-ri-music-fill">Tracks Saved</DTitle>
              <DDetail>{profile.saved_tracks}</DDetail>
              <DTitle className="i-ri-album-fill">Albums Saved</DTitle>
              <DDetail>{profile.saved_albums}</DDetail>
              <DTitle className="i-ri-folder-music-fill">
                Playlists Saved
              </DTitle>
              <DDetail>{profile.saved_playlists}</DDetail>
              <DTitle className="i-ri-mic-2-fill">Artists Followed</DTitle>
              <DDetail>{profile.saved_artists}</DDetail>
              <DTitle className="i-ri-headphone-fill">Shows Followed</DTitle>
              <DDetail>{profile.saved_shows}</DDetail>
            </DescriptionList>
          </section>
        </article>
      ) : null}
    </main>
  );
}
