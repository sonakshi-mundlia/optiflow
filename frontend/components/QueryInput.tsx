"use client";

import { useState } from "react";

type Props = {
  onSubmit: (query: string) => void | Promise<void>;
  loading: boolean;
};


export default function QueryInput({
  onSubmit,
  loading,
}: Props) {

  const [query, setQuery] = useState("");


  function handleSubmit() {

    const value = query.trim();

    if (!value || loading) {
      return;
    }

    onSubmit(value);
  }


  return (
    <div className="rounded-2xl border border-[#e7dfb6] bg-white p-5 shadow-[0_8px_30px_rgba(70,60,20,0.05)]">

      <div className="mb-3 flex items-center justify-between gap-4">

        <label className="text-sm font-semibold text-neutral-900">
          Ask OptiFlow
        </label>

        <span className="rounded-full bg-[#fff9d9] px-3 py-1 text-xs font-medium text-neutral-600">
          AI Query Router
        </span>

      </div>


      <textarea
        value={query}
        onChange={(event) =>
          setQuery(event.target.value)
        }
        onKeyDown={(event) => {

          if (
            event.key === "Enter" &&
            event.ctrlKey
          ) {
            event.preventDefault();
            handleSubmit();
          }

        }}
        placeholder="Ask a simple question or a complex technical problem..."
        rows={6}
        disabled={loading}
        className="
          w-full
          resize-none
          rounded-xl
          border
          border-[#e7dfb6]
          bg-[#fffef8]
          p-4
          text-sm
          text-neutral-900
          placeholder:text-neutral-400
          outline-none
          transition
          focus:border-[#cdbb4e]
          focus:ring-4
          focus:ring-[#f7efb8]
          disabled:cursor-not-allowed
          disabled:opacity-60
        "
      />


      <div className="mt-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">

        <div className="text-xs text-neutral-500">
          Ctrl + Enter to run
        </div>


        <button
          type="button"
          onClick={handleSubmit}
          disabled={
            loading ||
            !query.trim()
          }
          className="
            rounded-xl
            border
            border-[#d3c15a]
            bg-[#f6edaa]
            px-5
            py-2.5
            text-sm
            font-bold
            text-neutral-900
            transition
            hover:bg-[#efe39a]
            disabled:cursor-not-allowed
            disabled:opacity-50
          "
        >
          {loading
            ? "Processing..."
            : "Run Query"}
        </button>

      </div>

    </div>
  );
}