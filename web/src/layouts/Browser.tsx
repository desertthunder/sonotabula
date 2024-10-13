import { DashboardLayout } from "./Dashboard";

interface Props {
  children: React.ReactNode;
}

export function BrowserLayout({ children }: Props) {
  return <DashboardLayout>{children}</DashboardLayout>;
}
