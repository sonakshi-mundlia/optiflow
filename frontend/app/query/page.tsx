"use client";

import Link from "next/link";
import { useState } from "react";

import QueryInput from "../../components/QueryInput";
import AnswerPanel from "../../components/AnswerPanel";
import ExecutionOverview from "../../components/ExecutionOverview";
import MetricsGrid from "../../components/MetricsGrid";
import QueryHistory from "../../components/QueryHistory";

import {
  processQuery,
  type QueryResult,
} from "../../lib/api";


export default function QueryPage() {

  const [result, setResult] =
    useState<QueryResult | null>(null);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");

  const [historyRefresh, setHistoryRefresh] =
    useState(0);


  async function handleQuery(query: string) {

    try {

      setLoading(true);
      setError("");

      const data =
        await processQuery(query);

      setResult(data);

      setHistoryRefresh(
        (value) => value + 1
      );

    } catch (err) {

      setError(
        err instanceof Error
          ? err.message
          : "Failed to process query."
      );

    } finally {

      setLoading(false);

    }
  }


  return (
    <main className="min-h-screen bg-white text-[var(--text)]">

      {/* =====================================================
          HEADER
      ===================================================== */}

      <header className="border-b border-[var(--border)] bg-white">

        <div className="mx-auto flex max-w-6xl items-center justify-between px-5 py-4 lg:px-8">

          <Link
            href="/"
            className="flex items-center gap-3"
          >

            <div className="flex h-10 w-10 items-center justify-center rounded-xl brand-bg font-black">
              O
            </div>


            <div>

              <div className="font-bold">
                OptiFlow
              </div>

              <div className="text-xs muted">
                Query Workspace
              </div>

            </div>

          </Link>


          <Link
            href="/"
            className="text-sm font-semibold muted"
          >
            ← Home
          </Link>

        </div>

      </header>


      {/* =====================================================
          CONTENT
      ===================================================== */}

      <div className="mx-auto max-w-6xl px-5 py-12 lg:px-8">


        {/* TITLE */}

        <div className="mb-8">

          <div className="accent" />

          <p className="mt-4 text-xs font-bold uppercase tracking-widest brand">
            Query Workspace
          </p>

          <h1 className="mt-3 text-4xl font-black sm:text-5xl">
            Ask OptiFlow
          </h1>

          <p className="mt-3 max-w-2xl leading-7 muted">
            Enter your question and OptiFlow will analyze, check the cache,
            select a route, and return the answer with execution details.
          </p>

        </div>


        {/* INPUT */}

        <QueryInput
          onSubmit={handleQuery}
          loading={loading}
        />


        {/* ERROR */}

        {error && (

          <div className="red-light mt-4 rounded-xl border border-red-200 px-4 py-3">

            <div className="flex items-center gap-3">

              <span className="badge-red">
                Error
              </span>

              <span className="text-sm">
                {error}
              </span>

            </div>

          </div>

        )}


        {/* LOADING */}

        {loading && (

          <div className="card mt-6 p-6">

            <div className="flex items-center gap-3">

              <div className="h-5 w-5 animate-spin rounded-full border-2 border-[var(--yellow)] border-t-transparent" />

              <div>

                <p className="font-semibold">
                  Processing query...
                </p>

                <p className="mt-1 text-sm muted">
                  Analyzing query, checking cache, and selecting a route.
                </p>

              </div>

            </div>

          </div>

        )}


        {/* EMPTY STATE */}

        {!result && !loading && !error && (

          <div className="surface mt-8 rounded-2xl border border-[var(--border)] p-8">

            <div className="text-center">

              <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-xl brand-bg font-black">
                O
              </div>

              <h2 className="mt-4 text-xl font-bold">
                Ready to process your query
              </h2>

              <p className="mx-auto mt-2 max-w-xl text-sm leading-6 muted">
                Enter a question above to see the route, model, cache status,
                latency, cost, and other execution information.
              </p>


              {/* FLOW */}

              <div className="mt-6 flex flex-wrap items-center justify-center gap-2">

                <span className="badge-yellow">
                  Analyze
                </span>

                <span className="muted">
                  →
                </span>

                <span className="badge-green">
                  Cache
                </span>

                <span className="muted">
                  →
                </span>

                <span className="badge-blue">
                  Route
                </span>

                <span className="muted">
                  →
                </span>

                <span className="badge-yellow">
                  Answer
                </span>

              </div>

            </div>

          </div>

        )}


        {/* RESULT */}

        {result && (

          <div className="mt-8 space-y-5">

            <AnswerPanel
              result={result}
            />

            <ExecutionOverview
              result={result}
            />

            <MetricsGrid
              result={result}
            />

          </div>

        )}


        {/* HISTORY */}

        <div className="mt-8">

          <QueryHistory
            refreshToken={historyRefresh}
          />

        </div>

      </div>


      {/* FOOTER */}

      <footer className="border-t border-[var(--border)] bg-white py-6 text-center text-xs muted">
        OptiFlow • Intelligent AI Query Routing
      </footer>

    </main>
  );
}