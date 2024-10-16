import { Navbar, Sidebar } from "@/components";
import { useTokenValidator } from "@/libs/hooks";
import { useTokenStore } from "@/store";
import { useEffect } from "react";
import { useLocation } from "wouter";

export function DashboardLayout(props: { children: React.ReactNode }) {
  const query = useTokenValidator();
  const token = useTokenStore((state) => state.token);
  const [, navigate] = useLocation();

  useEffect(() => {
    if (!token) {
      navigate("/login", { replace: true });
    }
  }, [token, navigate]);

  if (query.isLoading) {
    return <div>Loading...</div>;
  }

  if (query.isError) {
    return <div>Error: {query.error.message}</div>;
  }

  return (
    <div className="flex flex-col h-screen bg-gradient-to-b from-emerald-600 to-50% via-emerald-500 via-50%">
      <Navbar />
      <section className="flex flex-1">
        <Sidebar />
        {props.children}
      </section>
    </div>
  );
}
