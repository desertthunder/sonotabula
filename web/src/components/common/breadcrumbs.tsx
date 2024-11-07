import capitalize from "lodash/capitalize";
import React, { useMemo } from "react";
import { Link, useRoute } from "wouter";

function usePathMatch(ctx: string) {
  const [base] = useRoute("/");
  const [dashboardMatch] = useRoute("/dashboard");
  const [contextMatch] = useRoute(`/dashboard/browser/${ctx}`);
  const [detailMatch] = useRoute(`/dashboard/browser/${ctx}/:id`);

  const routes = useMemo(() => {
    if (detailMatch) {
      return [
        { label: "Home", href: "/", match: base },
        { label: "Dashboard", href: "/dashboard", match: dashboardMatch },
        {
          label: `${capitalize(ctx.slice(0, -1))} Browser`,
          href: `/dashboard/browser/${ctx}`,
          match: contextMatch,
        },
        {
          label: `${capitalize(ctx.slice(0, -1))} Detail`,
          href: `/dashboard/browser/${ctx}/:id`,
          match: detailMatch,
        },
      ];
    }

    if (contextMatch) {
      return [
        { label: "Home", href: "/", match: base },
        { label: "Dashboard", href: "/dashboard", match: dashboardMatch },
        {
          label: `${capitalize(ctx.slice(0, -1))} Browser`,
          href: `/dashboard/browser/${ctx}`,
          match: contextMatch,
        },
      ];
    }

    if (dashboardMatch) {
      return [
        { label: "Home", href: "/", match: base },
        { label: "Dashboard", href: "/dashboard", match: dashboardMatch },
      ];
    }

    return [{ label: "Home", href: "/", match: base }];
  }, [base, dashboardMatch, contextMatch, detailMatch, ctx]);

  return routes;
}

export function Breadcrumbs({
  context,
  title,
}: {
  context: "playlists" | "albums" | "artists" | "tracks";
  title?: string;
}) {
  const routes = usePathMatch(context);

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
