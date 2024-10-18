import React from "react";
import { useRoute, Link } from "wouter";

interface SidebarLinkProps {
  href: string;
  linkText: string;
  icon?: string;
}

function SidebarLink({ href, linkText }: SidebarLinkProps): JSX.Element {
  const [isActive] = useRoute(href);
  const attrs = React.useMemo(() => {
    const internal = href.startsWith("~/") || !href.startsWith("http");

    return {
      target: internal ? undefined : "_blank",
      rel: internal ? undefined : "noopener noreferrer",
      disabled: !internal,
    };
  }, [href]);

  return (
    <Link
      href={href}
      target={attrs.target}
      rel={attrs.rel}
      className={[
        "hover:border-l-4 hover:border-l-jade-indicator p-4 text-sm font-medium hover:bg-slate-300",
        "sidebar-link",
        isActive ? "active" : "",
        attrs.disabled ? "cursor-none pointer-events-none text-zinc-500" : "",
      ].join(" ")}
    >
      <span className="ml-3">{linkText}</span>
    </Link>
  );
}

export function Sidebar() {
  return (
    <aside className="flex flex-col w-1/6 min-h-full">
      <section className="flex flex-col flex-1 overflow-y-scroll bg-slate-100 border-r border-slate-200 shadow-2xl">
        <section className="flex flex-col border-b border-b-black">
          <SidebarLink href="~/dashboard" linkText="Dashboard" />
          <SidebarLink
            href="~/dashboard/browser/playlists"
            linkText="Playlists"
          />
          <SidebarLink href="~/dashboard/browser/tracks" linkText="Tracks" />
          <SidebarLink href="~/dashboard/browser/albums" linkText="Albums" />
          {/* <SidebarLink href="/dashboard/browser/artists" linkText="Artists" /> */}
          {/* <SidebarLink href="/explorer" linkText="Explorer" />
        <SidebarLink href="/recently-played" linkText="Recently Played" />
        <SidebarLink href="/top-tracks" linkText="Top Tracks" />
        <SidebarLink href="/top-artists" linkText="Top Artists" /> */}
        </section>

        <section className="flex flex-col">
          <SidebarLink
            href="https://github.com/desertthunder/spotify-dashboard"
            linkText="GitHub"
          />
          <SidebarLink
            linkText="Spotify"
            href="https://developer.spotify.com/documentation/web-api/reference/#category-playlists"
          />
          <SidebarLink linkText="Help" href="https://desertthunder.github.io" />
        </section>
        <section className="flex flex-col flex-1 p-4 text-3xl gap-8">
          <div className="flex flex-col items-center gap-4 p-4 border border-black rounded-md">
            <span className="text-sm flex items-center gap-1">
              <i className="i-openmoji-electric-plug" />
              Powered by
            </span>
            <div className="flex gap-4">
              <i className="i-openmoji-musicbrainz" />
              <i className="i-ri-spotify-fill text-primary" />
            </div>
          </div>
          <div className="flex flex-col gap-4 p-4 border border-black rounded-md items-center">
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
      <div
        aria-roledescription="toolbar"
        className="border-t border-t-zinc-300 bg-zinc-200 p-4 sticky bottom-0 flex justify-between"
      >
        <button className="bg-zinc-100 rounded-full w-12 h-12 flex items-center justify-center">
          <i className="i-ri-settings-3-line" />
        </button>
        <button className="bg-zinc-100 rounded-full w-12 h-12 flex items-center justify-center">
          <i className="i-ri-logout-box-line" />
        </button>
        <button className="bg-zinc-100 rounded-full w-12 h-12 flex items-center justify-center">
          <i className="i-ri-information-2-fill" />
        </button>
      </div>
    </aside>
  );
}
