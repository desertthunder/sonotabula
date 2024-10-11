import { Navbar } from "./Navbar";
import { Sidebar } from "./Sidebar";
import { LibraryCard } from "./LibraryCard";
import { useTokenValidator } from "@/libs/hooks";
import { COUNT_KEYS } from "@/libs/types/api";
import { StatCard } from "./StatCard";

export default function Dashboard() {
  const { token } = useTokenValidator();

  if (!token) {
    return null;
  }

  return (
    <>
      <Navbar />
      <div className="flex pt-12 overflow-hidden text-sm text-white min-h-screen overscroll-none">
        <Sidebar />
        <div className="relative flex-1 overflow-y-auto overscroll-none lg:ml-64">
          <main className="main">
            <section className="p-6 pb-0 space-y-2">
              <h1 className="font-headings text-gray-50 text-[1.5rem] font-medium">
                Dashboard
              </h1>
              <h3 className="font-headings text-gray-200">
                View your stats and library at a glance.
              </h3>
            </section>
            <section className="grid grid-cols-12 p-6 flex-1 space-x-4">
              <div className="col-span-9 max-h-[620px]">
                <LibraryCard />
              </div>
              <div className="col-span-3 flex flex-col max-h-[620px]">
                {COUNT_KEYS.map((key) => (
                  <StatCard key={key} scope={key} />
                ))}
              </div>
            </section>
          </main>
        </div>
      </div>
    </>
  );
}
