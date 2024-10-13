import { Navbar, Sidebar } from "@/components";

interface Props {
  children: React.ReactNode;
}

export function DashboardLayout({ children }: Props) {
  return (
    <>
      <Navbar />
      <div className="flex pt-12 overflow-hidden text-sm text-white min-h-screen overscroll-none">
        <Sidebar />
        <div className="relative flex-1 overflow-y-auto overscroll-none lg:ml-64">
          <main className="main">{children}</main>
        </div>
      </div>
    </>
  );
}
