import React from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { useQuery, useQueryClient } from "@tanstack/react-query";

enum CardTitles {
  TopTracks = "Top Tracks",
  TopArtists = "Top Artists",
  RecentlyPlayed = "Recently Played",
  Playlists = "Playlists",
}

enum CardType {
  Top = "Top",
  Library = "Library",
  Recent = "Recent",
}

interface CardProps {
  title: CardTitles;
  value?: string;
  type?: CardType;
}

function CardRow({
  children,
  span = 2,
}: {
  children: React.ReactNode;
  span?: 1 | 2;
}) {
  if (span === 1) {
    return <div className="grid h-1/2">{children}</div>;
  }

  return (
    <div className="grid gap-8 xl:grid-cols-2 2xl:grid-cols-3 h-1/2 last:pb-8">
      {children}
    </div>
  );
}

function Card({ title, type = CardType.Top, value = "Some Value" }: CardProps) {
  return (
    <div className="card">
      <div className="flex-shrink-0">
        <span className="text-xl font-bold leading-none text-gray-900 sm:text-2xl ">
          {title}
        </span>
        <h3 className="text-base font-light text-gray-500">{type}</h3>
      </div>
      <div className="flex items-center justify-end flex-1 text-base font-medium text-gray-700">
        {value}
      </div>
    </div>
  );
}

function Navbar() {
  return (
    <nav className="fixed z-30 w-full bg-gray-100 border-b-4 border-green-500">
      <div className="py-1 px-8 font-sans font-bold flex justify-between items-center">
        <Link to="/" className="text-lg text-black flex-1">
          Dashspot
        </Link>
        <input
          type="text"
          placeholder="Search"
          className="border border-gray-300 p-2 px-3 rounded-lg w-1/4 ring-primary ring-1"
        />
      </div>
    </nav>
  );
}

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

function Sidebar() {
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

function useQueryParams(): Record<string, string> {
  const location = useLocation();
  const params = new URLSearchParams(location.search);

  return Object.fromEntries(params.entries());
}

export default function Dashboard() {
  const navigate = useNavigate();
  const params = useQueryParams();
  const queryClient = useQueryClient();
  const queryData = queryClient.getQueryData<{
    message: string;
    token: string;
  }>(["token"]);

  const token = React.useMemo(() => {
    if (params.token) {
      return params.token;
    } else {
      return queryData?.token ?? null;
    }
  }, [params.token, queryData]);

  const query = useQuery({
    queryKey: ["token"],
    queryFn: async () => {
      console.debug("Checking token validity");

      if (!token) {
        throw new Error("Token not found");
      }

      const response = await fetch("/api/validate", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error("Token invalid");
      }

      const data: { message: string; token: string } = await response.json();

      return data;
    },
    refetchInterval: 5 * 60 * 1000, // 5 minutes
  });

  React.useEffect(() => {
    if (query.isError) {
      navigate("/login");
    } else if (query.isSuccess && params.token) {
      navigate("/dashboard");
    }
  }, [query, navigate, params]);

  return (
    <>
      <Navbar />
      <div className="flex pt-12 overflow-hidden text-sm text-white min-h-screen overscroll-none">
        <Sidebar />
        <div className="relative flex-1 overflow-y-auto overscroll-none lg:ml-64">
          <main className="main">
            <section className="px-4 pt-6">
              <h1 className="font-headings text-gray-50 text-[1.5rem] font-semibold">
                Dashboard
              </h1>
              <h3 className="font-headings text-gray-200">
                View your stats and library at a glance.
              </h3>
            </section>
            <section className="p-6 flex-1 space-y-4">
              <CardRow span={1}>
                <Card title={CardTitles.TopArtists} />
              </CardRow>
              <CardRow>
                <Card title={CardTitles.RecentlyPlayed} />
                <Card title={CardTitles.TopTracks} />
              </CardRow>
              <CardRow>
                <Card title={CardTitles.RecentlyPlayed} />
                <Card title={CardTitles.TopTracks} />
              </CardRow>
            </section>
          </main>
        </div>
      </div>
    </>
  );
}
