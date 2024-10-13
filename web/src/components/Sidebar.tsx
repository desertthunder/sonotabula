import React from "react";
import { Link, useLocation } from "react-router-dom";

interface SidebarLinkProps {
  href: string;
  linkText: string;
}

function SidebarLink({ href, linkText }: SidebarLinkProps): JSX.Element {
  const location = useLocation();

  const attrs = React.useMemo(() => {
    const internal = href.startsWith("/") || !href.startsWith("http");

    return {
      internal,
      isActive:
        (internal && location.pathname === href) ||
        location.pathname.includes(href),
      target: internal ? undefined : "_blank",
      rel: internal ? undefined : "noopener noreferrer",
    };
  }, [location, href]);

  return (
    <Link
      to={href}
      target={attrs.target}
      rel={attrs.rel}
      className={`sidebar-link ${attrs.isActive ? "active" : ""}`}
    >
      <span className="ml-3">{linkText}</span>
    </Link>
  );
}

export function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="flex flex-col pt-5 overflow-y-auto min-h-fit">
        <div className="flex-1">
          <section>
            <SidebarLink href="/dashboard" linkText="Dashboard" />
            <SidebarLink href="/profile" linkText="Profile" />
            <SidebarLink href="/playlists" linkText="Playlists" />
            <SidebarLink href="/top-tracks" linkText="Top Tracks" />
            <SidebarLink href="/top-artists" linkText="Top Artists" />
            <SidebarLink href="/recently-played" linkText="Recently Played" />
            <SidebarLink href="/library" linkText="Library" />
          </section>
          <hr className="border-t border-slate-700" />
          <section>
            <SidebarLink
              href="https://github.com/desertthunder/dashspot"
              linkText="GitHub"
            />
            <SidebarLink
              linkText="Spotify"
              href="https://developer.spotify.com/documentation/web-api/reference/#category-playlists"
            />
            <SidebarLink
              linkText="Help"
              href="https://desertthunder.github.io"
            />
          </section>
        </div>
      </div>
      <div className="flex-1 lg:bg-slate-200" />
    </aside>
  );
}
