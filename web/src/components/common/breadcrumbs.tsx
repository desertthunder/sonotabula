import { Link, useRoute } from "wouter";
import React, { useMemo } from "react";

export function Breadcrumbs({ title }: { title?: string }) {
  const [base] = useRoute("/");
  const [dashboardMatch] = useRoute("/dashboard");
  const [playlistsMatch] = useRoute("/dashboard/browser/playlists");
  const [playlistsDetailMatch] = useRoute("/dashboard/browser/playlists/:id");

  const routes = useMemo(() => {
    if (playlistsDetailMatch) {
      return [
        { label: "Home", href: "/dashboard", match: dashboardMatch },
        {
          label: "Playlist Browser",
          href: "/dashboard/browser/playlists",
          match: playlistsMatch,
        },
        {
          label: "Playlist Details",
          href: "/dashboard/browser/playlists/:id",
          match: playlistsDetailMatch,
        },
      ];
    }

    if (playlistsMatch) {
      return [
        { label: "Home", href: "/dashboard", match: dashboardMatch },
        {
          label: "Playlist Browser",
          href: "/dashboard/browser/playlists",
          match: playlistsMatch,
        },
      ];
    }

    if (dashboardMatch) {
      return [
        { label: "Dashboard", href: "/dashboard", match: dashboardMatch },
      ];
    }

    return [{ label: "Home", href: "/", match: base }];
  }, [base, dashboardMatch, playlistsMatch, playlistsDetailMatch]);

  return (
    <header className="flex flex-col justify-between p-4 bg-white border-t">
      <p className="text-gray-500 flex items-center">
        {routes.map((link, index) => (
          <React.Fragment key={index}>
            <Link
              href={link.href}
              className={
                link.match ? "pointer-events-none" : "hover:text-emerald-500"
              }
            >
              <span className="group-hover:text-emerald-500">{link.label}</span>
            </Link>
            {index < routes.length - 1 && (
              <i className="i-ri-arrow-right-s-line align-middle" />
            )}
          </React.Fragment>
        ))}
      </p>
      <h1 className="text-2xl font-medium">
        {title ?? routes[routes.length - 1].label}
      </h1>
    </header>
  );
}
