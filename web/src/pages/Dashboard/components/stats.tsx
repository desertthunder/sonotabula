import { titleCase } from "@/libs/helpers";
import { useSavedCounts } from "@/libs/hooks";
import { CountKey } from "@/libs/types";

interface Props {
  scope: CountKey;
}

export function StatCard({ scope }: Props) {
  const context = useSavedCounts();

  return (
    <div className="rounded-xl bg-zinc-100 text-black shadow-lg flex">
      <div className="bg-gradient-to-br from-emerald-500 to-green-400 rounded-l-xl w-4" />
      <section className="flex flex-col gap-2 p-4 ">
        <h1 className="text-lg font-medium text-slate-900">
          {titleCase(scope)}
        </h1>
        {context.isLoading ? <span>Loading</span> : null}
        {context.isError ? <span>Error</span> : null}
        {context.data ? (
          <h2 className="text-4xl text-primary font-medium">
            {context.data[scope as CountKey]}
          </h2>
        ) : null}
      </section>
    </div>
  );
}
