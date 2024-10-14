import { useSavedCounts } from "@/libs/hooks";
import { CountKey } from "@/libs/types/api";

interface Props {
  scope: CountKey;
}

function titleCase(str: string) {
  return str[0].toUpperCase() + str.slice(1);
}

export function StatCard({ scope }: Props) {
  const context = useSavedCounts();

  return (
    <div className="rounded-xl border bg-white text-black shadow-lg border-l-8 border-l-emerald-400">
      <section className="flex flex-col gap-2 p-4">
        <h1 className="text-lg font-medium text-slate-9004">
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
