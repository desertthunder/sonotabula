import capitalize from "lodash/capitalize";
import React, { useMemo } from "react";
import { Link, useRoute } from "wouter";

export function Breadcrumbs({
  context,
  title,
}: {
  context: "playlists" | "albums";
  title?: string;
}) {
  const [base] = useRoute("/");
  const [dashboardMatch] = useRoute("/dashboard");
  const [playlistsMatch] = useRoute(`/dashboard/browser/${context}`);
  const [playlistsDetailMatch] = useRoute(`/dashboard/browser/${context}/:id`);

  const routes = useMemo(() => {
    const headerText = capitalize(context.slice(0, -1));
    if (playlistsDetailMatch) {
      return [
        { label: "Home", href: "/dashboard", match: dashboardMatch },
        {
          label: `${headerText} Browser`,
          href: `/dashboard/browser/${context}`,
          match: playlistsMatch,
        },
        {
          label: `${headerText} Detail`,
          href: `/dashboard/browser/${context}/:id`,
          match: playlistsDetailMatch,
        },
      ];
    }

    if (playlistsMatch) {
      return [
        { label: "Home", href: "/dashboard", match: dashboardMatch },
        {
          label: `${headerText} Browser`,
          href: `/dashboard/browser/${context}`,
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
  }, [base, dashboardMatch, playlistsMatch, playlistsDetailMatch, context]);

  return (
    <header className="flex flex-col justify-between p-4 bg-white border-t">
      <p className="text-gray-500 flex items-center">
        {routes.map((link, index) => (
          <React.Fragment key={index}>
            <Link
              href={link.href}
              className={
                link.match ? "pointer-events-none" : "hover:text-primary"
              }
            >
              <span className="group-hover:text-primary">{link.label}</span>
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
