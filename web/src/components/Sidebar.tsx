import { Flex, Separator } from "@radix-ui/themes";
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
          "hover:border-l-4 hover:border-l-jade-indicator p-4 text-sm font-medium",
          "sidebar-link",
          isActive ? "active" : "",
          attrs.disabled ? "cursor-none pointer-events-none" : "",
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
    <Flex
      height="100%"
      direction="column"
      minWidth="15%"
      className="bg-jade-3 border-r"
    >
      <Flex direction="column">
        <SidebarLink href="/dashboard" linkText="Dashboard" />
        <SidebarLink href="/dashboard/browser" linkText="Browser" />
        <SidebarLink href="/playlists" linkText="Playlists" />
        <SidebarLink href="/top-tracks" linkText="Top Tracks" />
        <SidebarLink href="/top-artists" linkText="Top Artists" />
        <SidebarLink href="/recently-played" linkText="Recently Played" />
        <SidebarLink href="/library" linkText="Library" />
      </Flex>
      <Separator orientation="horizontal" size="4" />
      <Flex direction="column" height="100%">
        <SidebarLink
          href="https://github.com/desertthunder/spotify-dashboard"
          linkText="GitHub"
        />
        <SidebarLink
          linkText="Spotify"
          href="https://developer.spotify.com/documentation/web-api/reference/#category-playlists"
        />
        <SidebarLink linkText="Help" href="https://desertthunder.github.io" />
      </Flex>
    </Flex>
  );
}
