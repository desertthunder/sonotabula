import { useNavigate, Outlet, useMatch } from "react-router-dom";
import { useEffect } from "react";

export function BrowserLayout() {
  const navigate = useNavigate();
  const match = useMatch("/dashboard/browser");

  useEffect(() => {
    if (match) {
      navigate("/dashboard/browser/playlists");
    }
  }, [navigate, match]);

  return <Outlet />;
}
