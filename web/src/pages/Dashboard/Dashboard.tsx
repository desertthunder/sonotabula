import { LibraryCard } from "./LibraryCard";
import { COUNT_KEYS } from "@/libs/types/api";
import { StatCard } from "./StatCard";

export default function Dashboard() {
  return (
    <>
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
    </>
  );
}
