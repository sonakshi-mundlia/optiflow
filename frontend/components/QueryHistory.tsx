"use client";

import { useEffect, useState } from "react";
import { getHistory } from "../lib/api";

type HistoryRow = {
  request_id: string;
  query: string;
  route: string;
  model: string;
  complexity: string;
  cache_hit: boolean;
  similarity: number | null;
  estimated_cost: number;
  latency_ms: number;
  quality_score: number;
  created_at: string;
};

type Props = {
  refreshToken: number;
};

export default function QueryHistory({
  refreshToken,
}: Props) {
  const [rows, setRows] = useState<HistoryRow[]>([]);
  const [loading, setLoading] = useState(false);

  async function loadHistory() {
    try {
      setLoading(true);

      const data = await getHistory();

      if (Array.isArray(data)) {
        setRows(data);
      } else {
        setRows([]);
      }
    } catch {
      setRows([]);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadHistory();
  }, [refreshToken]);

  if (loading && rows.length === 0) {
    return (
      <section className="card p-6">
        <div className="accent" />

        <p className="mt-4 text-xs font-bold uppercase tracking-widest brand">
          Activity
        </p>

        <h2 className="mt-2 text-xl font-bold">
          Recent Queries
        </h2>

        <p className="mt-4 text-sm muted">
          Loading history...
        </p>
      </section>
    );
  }

  if (!rows.length) {
    return null;
  }

  return (
    <section className="card p-6">

      {/* HEADER */}

      <div className="mb-6">

        <div className="accent" />

        <p className="mt-4 text-xs font-bold uppercase tracking-widest brand">
          Activity
        </p>

        <h2 className="mt-2 text-xl font-bold">
          Recent Queries
        </h2>

        <p className="mt-1 text-sm muted">
          Previous queries processed by OptiFlow.
        </p>

      </div>


      {/* HISTORY LIST */}

      <div className="space-y-3">

        {rows.map((row) => {

          const routeLabel =
            row.route === "semantic_cache"
              ? "Semantic Cache"
              : row.route === "small_llm"
                ? "Small LLM"
                : row.route === "large_llm"
                  ? "Large LLM"
                  : row.route.replaceAll("_", " ");

          return (
            <div
              key={row.request_id}
              className="
                rounded-xl
                border
                border-[var(--border)]
                bg-white
                p-4
                transition
                hover-yellow
              "
            >

              {/* TOP ROW */}

              <div className="flex flex-wrap items-center gap-2">

                {/* ROUTE */}

                {row.route === "semantic_cache" && (
                  <span className="badge-green">
                    {routeLabel}
                  </span>
                )}

                {row.route === "small_llm" && (
                  <span className="badge-blue">
                    {routeLabel}
                  </span>
                )}

                {row.route === "large_llm" && (
                  <span className="badge-red">
                    {routeLabel}
                  </span>
                )}

                {![
                  "semantic_cache",
                  "small_llm",
                  "large_llm",
                ].includes(row.route) && (
                  <span className="badge-yellow">
                    {routeLabel}
                  </span>
                )}


                {/* COMPLEXITY */}

                {row.complexity === "low" && (
                  <span className="badge-green">
                    Low
                  </span>
                )}

                {row.complexity === "medium" && (
                  <span className="badge-yellow">
                    Medium
                  </span>
                )}

                {row.complexity === "high" && (
                  <span className="badge-red">
                    High
                  </span>
                )}


                {/* CACHE HIT */}

                {row.cache_hit && (
                  <span className="badge-green">
                    Cache Hit
                  </span>
                )}

              </div>


              {/* QUERY */}

              <p className="mt-3 text-sm leading-6 text-[var(--text)]">
                {row.query}
              </p>


              {/* METRICS */}

              <div className="mt-4 flex flex-wrap items-center gap-x-5 gap-y-2 text-xs muted">

                <span>
                  Latency:{" "}
                  <strong className="text-[var(--text)]">
                    {row.latency_ms.toFixed(0)} ms
                  </strong>
                </span>


                <span>
                  Cost:{" "}
                  <strong className="text-[var(--text)]">
                    ${row.estimated_cost.toFixed(6)}
                  </strong>
                </span>


                <span>
                  Quality:{" "}
                  <strong className="green-text">
                    {(row.quality_score * 100).toFixed(0)}%
                  </strong>
                </span>


                {row.similarity !== null && (
                  <span>
                    Similarity:{" "}
                    <strong className="brand">
                      {row.similarity.toFixed(3)}
                    </strong>
                  </span>
                )}

              </div>


              {/* MODEL + DATE */}

              <div className="mt-3 flex flex-wrap items-center justify-between gap-2 border-t border-[var(--border)] pt-3 text-xs muted">

                <span>
                  Model: {row.model}
                </span>

                <span>
  {row.created_at
    ? new Date(`${row.created_at}Z`).toLocaleString("en-IN", {
        timeZone: "Asia/Kolkata",
        day: "2-digit",
        month: "short",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        hour12: true,
      })
    : "Unknown time"}
</span>

              </div>

            </div>
          );
        })}

      </div>

    </section>
  );
}