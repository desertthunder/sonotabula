/**
 * @todo add proper static pages
 * @todo tracks page
 * @todo artists page
 */
import { Routes } from "@libs/types";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import { Route, Router, Switch } from "wouter";
import { Home, Profile, Signup } from "./pages";
import { Dashboard, DashboardLayout } from "./pages/Dashboard";
import { PlaylistsBrowser } from "./pages/Dashboard/Browser";
import { PlaylistDetailPage } from "./pages/Dashboard/Browser/Playlists/detail";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
    },
  },
});

export function AppRouter() {
  return (
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
          <Route path="/dashboard/browser/playlists/:id">
            <PlaylistDetailPage />
          </Route>
          <Route path="/dashboard/browser/playlists">
            <PlaylistsBrowser />
          </Route>
        </DashboardLayout>
      </Router>
    </Switch>
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
