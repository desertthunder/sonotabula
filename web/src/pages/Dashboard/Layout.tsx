import { Navbar, Sidebar } from "@/components";
import { useTokenValidator } from "@/libs/hooks";
import { useTokenStore } from "@/store";
import { Flex } from "@radix-ui/themes";
import { useEffect } from "react";
import { Outlet, useNavigate } from "react-router-dom";

export function DashboardLayout() {
  const query = useTokenValidator();
  const token = useTokenStore((state) => state.token);
  const navigate = useNavigate();

  useEffect(() => {
    if (!token) {
      navigate("/login");
    } else {
      navigate("/dashboard");
    }
  }, [token, navigate]);

  if (query.isLoading) {
    return <div>Loading...</div>;
  }

  if (query.isError) {
    return <div>Error: {query.error.message}</div>;
  }

  return (
    <Flex
      direction="column"
      className="h-screen bg-gradient-to-b from-emerald-600 to-50% via-emerald-500 via-50%"
    >
      <Navbar />
      <Flex flexGrow="1">
        <Sidebar />

        <Outlet />
      </Flex>
    </Flex>
  );
}
