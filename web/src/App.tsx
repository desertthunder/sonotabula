/**
 * @todo move routes enum to a libs/types
 * @todo add proper static pages
 */
import "./styles/base.css";
import "@fontsource-variable/inter";
import { Query, QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { Signup } from "./pages";
import { Dashboard, DashboardLayout } from "./pages/Dashboard";
import { BrowserLayout, BrowserPage } from "./pages/Browser";
import { createSyncStoragePersister } from "@tanstack/query-sync-storage-persister";
import { persistQueryClient } from "@tanstack/react-query-persist-client";
import { Playlist } from "./pages/Browser/Playlist";
import { BrowseAlbumsPage } from "./pages/Browser/Albums";

enum Routes {
  Home = "/",
  Signup = "/signup",
  Login = "/login",
  Dashboard = "/dashboard",
}

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
    },
  },
});

const localStoragePersister = createSyncStoragePersister({
  storage: window.localStorage,
});

persistQueryClient({
  queryClient,
  persister: localStoragePersister,
  dehydrateOptions: {
    shouldDehydrateQuery(query: Query): boolean {
      // We're only persisting the token query
      // but also want to keep the default behavior.
      return query.queryKey[0] === "token" && query.state.status === "success";
    },
  },
});

export const BrowserRouter = createBrowserRouter([
  {
    path: Routes.Home,
    element: <Signup />,
  },
  {
    path: Routes.Login,
    element: <Signup />,
  },
  {
    path: Routes.Dashboard,
    element: <DashboardLayout />,
    children: [
      {
        path: "/dashboard",
        element: <Dashboard />,
      },
      {
        path: "/dashboard/browser",
        element: <BrowserLayout />,
        children: [
          {
            path: "/dashboard/browser/playlists",
            element: <BrowserPage />,
            children: [
              {
                path: "/dashboard/browser/playlists/:id",
                element: <Playlist />,
              },
            ],
          },
          {
            path: "/dashboard/browser/albums",
            element: <BrowseAlbumsPage />,
          },
        ],
      },
    ],
  },
]);

export default function Root() {
  return (
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={BrowserRouter} />
    </QueryClientProvider>
  );
}
