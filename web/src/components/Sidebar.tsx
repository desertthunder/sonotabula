import React from "react";
import { Link } from "wouter";

interface SidebarLinkProps {
  href: string;
  linkText: string;
  children?: React.ReactNode;
  disabled?: boolean;
}

function Toolbar() {
  return (
    <div
      aria-roledescription="toolbar"
      className={[
        "drop-shadow-xl shadow-xl",
        "border-t border-t-zinc-300 bg-emerald-500",
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
        href="https://dashspot-dev.netlify.app"
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
  linkText,
  children,
  disabled = false,
}: SidebarLinkProps): JSX.Element {
  const internal = href.startsWith("/");
  const attrs = React.useMemo(() => {
    const internal = href.startsWith("~/") || !href.startsWith("http");

    return {
      target: internal ? undefined : "_blank",
      rel: internal ? undefined : "noopener noreferrer",
      disabled,
    };
  }, [href, disabled]);
  if (internal) {
    return (
      <Link
        href={href}
        className={(active) => {
          return [
            active
              ? "border-l-4 bg-zinc-200 border-l-emerald-500 pointer-events-none"
              : "",
            "hover:border-l-4 hover:border-l-jade-indicator",
            "p-4 text-sm font-medium hover:bg-slate-300",
            "flex items-center gap-2 align-middle",
            attrs.disabled ? "cursor-none pointer-events-none" : "",
          ].join(" ");
        }}
      >
        {children}
        <span>{linkText}</span>
      </Link>
    );
  }

  return (
    <a
      href={href}
      target={attrs.target}
      rel={attrs.rel}
      className={[
        "hover:border-l-4 hover:border-l-jade-indicator",
        "p-4 text-sm font-medium hover:bg-slate-300",
        "flex items-center gap-2 align-middle",
        attrs.disabled ? "cursor-none pointer-events-none text-zinc-500" : "",
      ].join(" ")}
    >
      {children}
      <span>{linkText}</span>
    </a>
  );
}

export function Sidebar() {
  return (
    <aside className="flex flex-col w-1/6 min-h-full">
      <section className="no-scrollbar flex flex-col flex-1 overflow-y-scroll bg-zinc-100 border-r-[0.5px] border-zinc-100 shadow-2xl">
        <section className="flex flex-col border-b-[0.5px] border-b-black">
          <SidebarLink href="/" linkText="Dashboard" />
          <SidebarLink href="/browser/playlists" linkText="Playlists" />
          <SidebarLink href="/browser/tracks" linkText="Tracks" />
          <SidebarLink href="/browser/albums" linkText="Albums" />
          {/* <SidebarLink href="/dashboard/browser/artists" linkText="Artists" /> */}
          {/* <SidebarLink href="/explorer" linkText="Explorer" /> */}
          {/* <SidebarLink href="/recently-played" linkText="Recently Played" /> */}
          {/* <SidebarLink href="/top-tracks" linkText="Top Tracks" /> */}
          {/* <SidebarLink href="/top-artists" linkText="Top Artists" /> */}
        </section>

        <section className="flex flex-col">
          <SidebarLink
            href="https://github.com/desertthunder/spotify-dashboard"
            linkText="GitHub"
          >
            <i className="i-ri-github-fill" />
          </SidebarLink>
          <SidebarLink
            linkText="Spotify API Docs"
            href="https://developer.spotify.com/documentation/web-api/reference/#category-playlists"
          >
            <i className="i-ri-spotify-fill" />
          </SidebarLink>
          <SidebarLink
            linkText="Help"
            href="https://desertthunder.github.io"
            disabled
          >
            <i className="i-ri-questionnaire-fill" />
          </SidebarLink>
        </section>
        <section className="flex flex-col flex-1 p-4 text-3xl gap-8">
          <div
            className={[
              "flex flex-col items-center gap-4",
              "p-4 border-[0.5px] border-slate-400 bg-white",
              "drop-shadow-md rounded-md",
            ].join(" ")}
          >
            <span className="text-sm flex items-center gap-1">
              <i className="i-openmoji-electric-plug" />
              Powered by
            </span>
            <div className="flex gap-4">
              <i className="i-openmoji-musicbrainz" />
              <i className="i-ri-spotify-fill text-primary" />
            </div>
          </div>
          <div
            className={[
              "flex flex-col gap-4 p-4",
              "border-[0.5px] border-slate-400 drop-shadow-md rounded-md items-center bg-white",
            ].join(" ")}
          >
            <span className="text-sm">
              Built with <i className="i-openmoji-heart-suit" /> using
            </span>
            <div className="flex gap-4 flex-1">
              <i className="i-devicon-plain-postgresql text-secondary" />
              <i className="i-devicon-plain-django text-primary" />
              <i className="i-devicon-react" />
            </div>
          </div>
        </section>
      </section>
      <Toolbar />
    </aside>
  );
}
