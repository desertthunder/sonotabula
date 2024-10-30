/**
 * @todo add proper static pages
 * @todo tracks page
 * @todo artists page
 */
import { Routes } from "@libs/types";
import { createSyncStoragePersister } from "@tanstack/query-sync-storage-persister";
import { Query, QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import { persistQueryClient } from "@tanstack/react-query-persist-client";
import { Route, Router, Switch } from "wouter";
import { Home, Signup, Profile } from "./pages";
import { BrowserLayout } from "./pages/Browser";
import { BrowseAlbumsPage as BrowserAlbums } from "./pages/Browser/Albums";
import { Playlist } from "./pages/Browser/Playlist";
import { PlaylistsPage as BrowserPlaylists } from "./pages/Browser/Playlists";
import { TracksPage as BrowserTracks } from "./pages/Browser/Tracks";
import { Dashboard } from "./pages/Dashboard";
import { DashboardLayout } from "./pages/Dashboard/layout";

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
      <Switch>
        <Route path={Routes.Home}>
          <Home />
        </Route>
        <Route path={Routes.Signup}>
          <Signup />
        </Route>
        <Route path={Routes.Login}>
          <Signup />
        </Route>
        <Router>
          <DashboardLayout>
            <Route path="/dashboard">
              <Dashboard />
            </Route>
            <Route path="/dashboard/profile">
              <Profile />
            </Route>
            <Route path="/dashboard/browser" nest>
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
        </Router>
      </Switch>
    </>
  );
}

export default function Root() {
  return (
    <QueryClientProvider client={queryClient}>
      <AppRouter />
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
