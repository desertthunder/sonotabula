import "./App.css";
import "@fontsource-variable/noto-sans-jp";
import "@fontsource-variable/rubik";

import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { Signup, Dashboard } from "./pages";

enum Routes {
  Home = "/",
  Signup = "/signup",
  Login = "/login",
  Dashboard = "/dashboard/",
}

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
    element: <Dashboard />,
  },
]);

export default function Root() {
  return <RouterProvider router={BrowserRouter} />;
}
