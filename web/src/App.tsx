import "./styles/base.css";
import "@fontsource-variable/inter";
import "@fontsource-variable/rubik";
import "@fontsource-variable/noto-sans-jp";
import { Query, QueryClient, QueryClientProvider } from "@tanstack/react-query";
import {
  createBrowserRouter,
  LoaderFunction,
  RouterProvider,
} from "react-router-dom";
import { Signup, Dashboard, Browser } from "./pages";
import { createSyncStoragePersister } from "@tanstack/query-sync-storage-persister";
import { persistQueryClient } from "@tanstack/react-query-persist-client";
import { DashboardLayout } from "./layouts";
import { Playlist } from "./pages/Browser/Playlist";
import { playlistTracksLoader } from "./libs/hooks/api/loaders";

// TODO: Move to libs
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
    // TODO: Add a home page
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
        element: <Browser />,
        children: [
          {
            path: "/dashboard/browser/playlist/:id",
            element: <Playlist />,
            loader: playlistTracksLoader(queryClient) as LoaderFunction<{
              playlist: Record<string, string>;
              tracks: Array<Record<string, string>>;
            }>,
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
