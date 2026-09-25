import type { QueryResult } from "../lib/api";

type Props = {
  result: QueryResult | null;
};


export default function ExecutionOverview({
  result,
}: Props) {

  if (!result) {
    return null;
  }


  const items = [

    {
      label: "Complexity",
      value: result.complexity,
    },

    {
      label: "Route",
      value: result.route.replaceAll("_", " "),
    },

    {
      label: "Model",
      value: result.model,
    },

    {
      label: "Cache",
      value: result.cache_hit
        ? result.similarity !== null
          ? `Hit (${result.similarity.toFixed(3)})`
          : "Hit"
        : "Miss",
    },

  ];


  return (
    <section className="rounded-2xl border border-[#e7dfb6] bg-white p-5 shadow-[0_8px_30px_rgba(70,60,20,0.05)]">

      <div className="mb-4">

        <p className="text-xs font-semibold uppercase tracking-[0.16em] text-neutral-400">
          Routing Details
        </p>

        <h2 className="mt-1 text-lg font-bold text-neutral-900">
          Execution Overview
        </h2>

      </div>


      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">

        {items.map((item) => (

          <div
            key={item.label}
            className="rounded-xl border border-[#eee7c9] bg-[#fffdf2] p-4"
          >

            <div className="text-xs uppercase tracking-wide text-neutral-500">
              {item.label}
            </div>

            <div className="mt-2 truncate text-sm font-bold capitalize text-neutral-900">
              {item.value}
            </div>

          </div>

        ))}

      </div>

    </section>
  );
}