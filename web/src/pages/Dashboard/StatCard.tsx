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
    <div className="card stat flex-1 p-4 border-l-green-500 border-l-8">
      <header>
        <h1 className="text-lg font-medium text-slate-900">
          {titleCase(scope)}
        </h1>
      </header>
      <main>
        {context.isLoading ? <span>Loading</span> : null}
        {context.isError ? <span>Error</span> : null}
        {context.data ? (
          <span className="text-4xl text-primary">
            {context.data[scope as CountKey]}
          </span>
        ) : null}
      </main>
    </div>
  );
}
