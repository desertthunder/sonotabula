import React from "react";
import { NavLink } from "react-router-dom";

interface SidebarLinkProps {
  href: string;
  linkText: string;
}

function SidebarLink({ href, linkText }: SidebarLinkProps): JSX.Element {
  const attrs = React.useMemo(() => {
    const internal = href.startsWith("/") || !href.startsWith("http");

    return {
      target: internal ? undefined : "_blank",
      rel: internal ? undefined : "noopener noreferrer",
      disabled: internal && !href.includes("dashboard"),
    };
  }, [href]);

  return (
    <NavLink
      to={href}
      target={attrs.target}
      rel={attrs.rel}
      className={({ isActive }) =>
        [
          "hover:border-l-4 hover:border-l-jade-indicator p-4 text-sm font-medium hover:bg-slate-300",
          "sidebar-link",
          isActive ? "active" : "",
          attrs.disabled ? "cursor-none pointer-events-none text-zinc-500" : "",
        ].join(" ")
      }
      end={!href.includes("browser")}
    >
      <span className="ml-3">{linkText}</span>
    </NavLink>
  );
}

export function Sidebar() {
  return (
    <section className="flex flex-col h-full bg-slate-200 border-r w-1/6 shadow-2xl">
      <section className="flex flex-col border-b border-b-black">
        <SidebarLink href="/dashboard" linkText="Dashboard" />
        <SidebarLink href="/dashboard/browser" linkText="Browser" />
        <SidebarLink href="/playlists" linkText="Playlists" />
        <SidebarLink href="/top-tracks" linkText="Top Tracks" />
        <SidebarLink href="/top-artists" linkText="Top Artists" />
        <SidebarLink href="/recently-played" linkText="Recently Played" />
        <SidebarLink href="/library" linkText="Library" />
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
