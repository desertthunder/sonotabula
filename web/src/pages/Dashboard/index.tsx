import { Library } from "./Library";
import { Counts } from "@/libs/types/api";
import { StatCard } from "./components/Stats";

export function Dashboard() {
  return (
    <main
      className={[
        "bg-gradient-to-b from-emerald-600 to-50% via-emerald-500 via-50%",
        "flex-1 flex justify-between gap-8",
        "px-8 pt-4",
      ].join(" ")}
    >
      <section className="flex flex-col gap-4 flex-1 text-sm">
        <h1 className="text-base font-semibold text-zinc-100">Dashboard</h1>
        <p className="text-zinc-100">
          View your stats and library at a glance.
        </p>
        <div className="flex flex-col flex-1">
          <Library />
        </div>
      </section>

      <section className="flex flex-col gap-4 min-w-[25%]">
        {Counts.map((key) => (
          <StatCard key={key} scope={key} />
        ))}
      </section>
    </main>
  );
}

export { DashboardLayout } from "./Layout";
