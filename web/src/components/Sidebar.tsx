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
    <section className="flex flex-col h-full bg-slate-100 border-r border-slate-200 w-1/6 shadow-2xl">
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

      <section className="flex flex-col flex-1">
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
    </section>
  );
}
