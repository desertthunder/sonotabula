/**
 * @todo move routes enum to a libs/types
 * @todo add proper static pages
 * @todo tracks page
 * @todo artists page
 */
import "@fontsource-variable/inter";
import { createSyncStoragePersister } from "@tanstack/query-sync-storage-persister";
import { Query, QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { persistQueryClient } from "@tanstack/react-query-persist-client";
import { Route } from "wouter";
import { Signup } from "./pages";
import { BrowserLayout } from "./pages/Browser";
import { BrowseAlbumsPage as BrowserAlbums } from "./pages/Browser/Albums";
import { Playlist } from "./pages/Browser/Playlist";
import { PlaylistsPage as BrowserPlaylists } from "./pages/Browser/Playlists";
import { Dashboard, DashboardLayout } from "./pages/Dashboard";
import { TracksPage as BrowserTracks } from "./pages/Browser/Tracks";
import "./styles/base.css";

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

export function AppRouter() {
  return (
    <>
      <Route path={Routes.Home}>
        <Signup />
      </Route>
      <Route path={Routes.Login}>
        <Signup />
      </Route>
      <Route path={Routes.Dashboard} nest>
        <DashboardLayout>
          <Route path="/">
            <Dashboard />
          </Route>
          <Route path="/browser" nest>
            <BrowserLayout>
              <Route path="/playlists" nest>
                <BrowserPlaylists>
                  <Route path="/:id">
                    <Playlist />
                  </Route>
                </BrowserPlaylists>
              </Route>
              <Route path="/albums">
                <BrowserAlbums />
              </Route>
              <Route path="/tracks">
                <BrowserTracks />
              </Route>
            </BrowserLayout>
          </Route>
        </DashboardLayout>
      </Route>
    </>
  );
}

export default function Root() {
  return (
    <QueryClientProvider client={queryClient}>
      <AppRouter />
    </QueryClientProvider>
  );
}
