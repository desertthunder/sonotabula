import { Navbar, Sidebar } from "@/components";
import { useTokenValidator } from "@/libs/hooks";
import { useEffect } from "react";
import { Outlet, useNavigate } from "react-router-dom";

export function DashboardLayout() {
  const { query, token } = useTokenValidator();
  const navigate = useNavigate();

  useEffect(() => {
    if (query.isFetching || query.isLoading) {
      return;
    }

    if (!token) {
      navigate("/login");
    } else {
      navigate("/dashboard");
    }
  }, [token, query.isFetching, query.isLoading, navigate]);

  if (query.isLoading) {
    return <div>Loading...</div>;
  }

  if (query.isError) {
    return <div>Error: {query.error.message}</div>;
  }

  return (
    <>
      <Navbar />
      <div className="flex pt-12 overflow-hidden text-sm text-white min-h-screen overscroll-none">
        <Sidebar />
        <div className="relative flex-1 overflow-y-auto overscroll-none lg:ml-64">
          <main className="main">
            <Outlet />
          </main>
        </div>
      </div>
    </>
  );
}
