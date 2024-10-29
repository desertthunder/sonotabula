import { titleCase } from "@libs/helpers";
import { useSavedCounts } from "@libs/hooks";
import { CountKey } from "@libs/types";

interface Props {
  scope: CountKey;
}

export function StatCard({ scope }: Props) {
  const context = useSavedCounts();

  return (
    <div className="rounded-xl bg-zinc-100 text-black shadow-lg flex flex-1 hover:rotate-12 transition-transform duration-200">
      <div className="bg-gradient-to-br from-emerald-500 to-green-400 rounded-l-lg w-4" />
      <section className="flex flex-col px-3 py-2">
        <h1 className="text-lg font-semibold tracking-tight font-headings text-slate-800">
          {titleCase(scope)}
        </h1>
        {context.isLoading ? <span>Loading</span> : null}
        {context.isError ? <span>Error</span> : null}
        {context.data ? (
          <h2 className="text-xl text-primary font-medium font-titles">
            {context.data[scope as CountKey]}
          </h2>
        ) : null}
      </section>
    </div>
  );
}
