import { useNavigate, Outlet } from "react-router-dom";
import { useEffect } from "react";

export function BrowserLayout() {
  const navigate = useNavigate();

  useEffect(() => {
    navigate("/dashboard/browser/playlists");
  }, [navigate]);

  return <Outlet />;
}
