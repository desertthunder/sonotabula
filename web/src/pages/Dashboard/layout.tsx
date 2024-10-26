import { Navbar, Sidebar } from "@/components";
import { useTokenValidator } from "@libs/hooks";
import { useTokenStore } from "@/store";
import { useEffect } from "react";
import { useLocation, useSearch } from "wouter";

export function DashboardLayout(props: { children: React.ReactNode }) {
  const query = useTokenValidator();
  const setToken = useTokenStore((state) => state.setToken);
  const [, navigate] = useLocation();
  const searchParams = useSearch();

  useEffect(() => {
    const params = new URLSearchParams(searchParams);
    if (params.get("token")) {
      setToken(params.get("token") as string);
      navigate("/");
    }
  }, [setToken, navigate, searchParams]);

  if (query.isLoading) {
    return <div>Loading...</div>;
  }

  if (query.isError) {
    return <div>Error: {query.error.message}</div>;
  }

  return (
    <div
      className={[
        "flex flex-col max-h-screen",
        "min-h-screen",
        "bg-gradient-to-b from-emerald-600 to-50% via-emerald-500 via-50%",
      ].join(" ")}
    >
      <Navbar />
      <section className="flex flex-1 overflow-auto">
        <Sidebar />
        {props.children}
      </section>
    </div>
  );
}
