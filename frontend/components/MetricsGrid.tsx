import type { QueryResult } from "../lib/api";

type Props = {
  result: QueryResult | null;
};


export default function MetricsGrid({
  result,
}: Props) {

  if (!result) {
    return null;
  }


  const metrics = [

    {
      label: "Latency",
      value: `${result.latency_ms.toFixed(0)} ms`,
    },

    {
      label: "Estimated Cost",
      value: `$${result.estimated_cost.toFixed(6)}`,
    },

    {
      label: "Quality",
      value: `${(
        result.quality_score * 100
      ).toFixed(0)}%`,
    },

    {
      label: "Router Score",
      value: result.router_score.toFixed(3),
    },

    {
      label: "Input Tokens",
      value: result.input_tokens.toString(),
    },

    {
      label: "Output Tokens",
      value: result.output_tokens.toString(),
    },

  ];


  return (
    <section>

      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">

        {metrics.map((metric) => (

          <div
            key={metric.label}
            className="rounded-xl border border-[#e7dfb6] bg-[#fffdf2] p-5"
          >

            <div className="text-xs uppercase tracking-wide text-neutral-500">
              {metric.label}
            </div>

            <div className="mt-2 text-xl font-bold text-neutral-900">
              {metric.value}
            </div>

          </div>

        ))}

      </div>


      <p className="mt-3 text-xs text-neutral-500">
        Quality is an explainable response-completeness heuristic for the MVP.
      </p>

    </section>
  );
}