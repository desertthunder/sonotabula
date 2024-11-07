import React from "react";
import { Link, useRoute } from "wouter";

interface SidebarLinkProps {
  href: string;
  label: string;
  children?: React.ReactNode;
  disabled?: boolean;
  isActive?: boolean;
}

function Toolbar() {
  return (
    <div
      aria-roledescription="toolbar"
      className={[
        "drop-shadow-xl shadow-xl",
        "border-t border-t-zinc-300 bg-primary",
        "p-4 sticky bottom-0 flex justify-between",
        "text-slate-800",
      ].join(" ")}
    >
      <button className="bg-zinc-100 rounded-full flex items-center justify-center w-12 h-12 group">
        <i className="i-ri-settings-5-fill w-6 h-6 group-hover:scale-110 transition-transform duration-500" />
      </button>
      <button className="bg-zinc-100 rounded-full flex items-center justify-center w-12 h-12 group">
        <i className="i-ri-logout-circle-line w-6 h-6 group-hover:scale-110 transition-transform duration-500" />
      </button>
      <a
        href="https://sonotabula.netlify.app"
        rel="noopener noreferrer"
        target="_blank"
        className="bg-zinc-100 rounded-full flex items-center justify-center w-12 h-12 group"
      >
        <i className="i-ri-information-2-fill w-6 h-6 group-hover:scale-110 transition-transform duration-500" />
      </a>
    </div>
  );
}

function SidebarLink({
  href,
  label,
  children,
  isActive = false,
  disabled = false,
}: SidebarLinkProps): JSX.Element {
  const attrs = React.useMemo(() => {
    const internal = href.startsWith("~/") || !href.startsWith("http");

    return {
      target: internal ? undefined : "_blank",
      rel: internal ? undefined : "noopener noreferrer",
      disabled,
    };
  }, [href, disabled]);
  return (
    <Link
      to={href}
      className={[
        isActive ? "border-l-4 bg-zinc-200 border-l-primary" : "",
        disabled || isActive ? "pointer-events-none" : "",
        disabled ? "text-gray-500" : "",
        "hover:border-l-4 hover:border-l-primary",
        "p-4 text-sm font-medium hover:bg-slate-300",
        "flex items-center gap-2 align-middle",
      ].join(" ")}
      {...attrs}
    >
      {children}
      <span>{label}</span>
    </Link>
  );
}

function ExternalLinks() {
  return (
    <section className="flex flex-col">
      <SidebarLink
        href="https://github.com/desertthunder/spotify-dashboard"
        label="GitHub"
      >
        <i className="i-ri-github-fill" />
      </SidebarLink>
      <SidebarLink
        label="Spotify API Docs"
        href="https://developer.spotify.com/documentation/web-api/reference/#category-playlists"
      >
        <i className="i-ri-spotify-fill" />
      </SidebarLink>
      <SidebarLink label="Help" href="https://desertthunder.github.io" disabled>
        <i className="i-ri-questionnaire-fill" />
      </SidebarLink>
    </section>
  );
}

function InfoBox({ children }: { children: React.ReactNode }) {
  return (
    <div
      className={[
        "flex flex-col items-center gap-4",
        "p-4 border-[0.5px] border-slate-400 bg-white",
        "drop-shadow-md rounded-md",
      ].join(" ")}
    >
      {children}
    </div>
  );
}

export function Sidebar() {
  const [playlistsMatch] = useRoute("/dashboard/browser/playlists/*?");
  const [albumsMatch] = useRoute("/dashboard/browser/albums/*?");
  const [dashboardMatch] = useRoute("/dashboard");

  return (
    <aside className="flex flex-col w-1/6 min-h-full">
      <div className="no-scrollbar flex flex-col flex-1 overflow-y-scroll bg-zinc-100 border-r-[0.5px] border-zinc-100 shadow-2xl divide-y-[0.5px] divide-black">
        <section className="flex flex-col">
          <SidebarLink
            href="/dashboard"
            label="Dashboard"
            isActive={dashboardMatch}
          />
          <SidebarLink
            href="/dashboard/browser/playlists"
            label="Playlists"
            isActive={playlistsMatch}
          />
          <SidebarLink
            href="/dashboard/browser/albums"
            label="Albums"
            isActive={albumsMatch}
          />
          <SidebarLink
            href="/dashboard/browser/tracks"
            label="Tracks"
            disabled
          />
        </section>

        <ExternalLinks />
        <section className="flex flex-col flex-1 p-4 text-3xl gap-8 justify-end">
          <InfoBox>
            <span className="text-sm flex items-center gap-1">
              <i className="i-openmoji-electric-plug" />
              Powered by
            </span>
            <div className="flex gap-4">
              <i className="i-openmoji-musicbrainz" />
              <i className="i-ri-spotify-fill text-primary" />
            </div>
          </InfoBox>
          <InfoBox>
            <span className="text-sm">
              Built with <i className="i-openmoji-heart-suit" /> using
            </span>
            <div className="flex gap-4 flex-1">
              <i className="i-devicon-plain-postgresql text-secondary" />
              <i className="i-devicon-plain-django text-primary" />
              <i className="i-devicon-react" />
            </div>
          </InfoBox>
        </section>
      </div>
      <Toolbar />
    </aside>
  );
}
