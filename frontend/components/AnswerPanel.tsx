import type { QueryResult } from "../lib/api";

type Props = {
  result: QueryResult | null;
};


export default function AnswerPanel({
  result,
}: Props) {

  if (!result) {
    return null;
  }


  return (
    <section className="rounded-2xl border border-[#e7dfb6] bg-white p-6 shadow-[0_8px_30px_rgba(70,60,20,0.05)]">

      <div className="mb-5 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">

        <div>

          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-neutral-400">
            Response
          </p>

          <h2 className="mt-1 text-lg font-bold text-neutral-900">
            Final Answer
          </h2>

        </div>


        <span className="w-fit rounded-full border border-[#e5ddb8] bg-[#faf6df] px-3 py-1.5 text-xs font-bold capitalize text-neutral-700">
          {result.route.replaceAll("_", " ")}
        </span>

      </div>


      <div className="rounded-xl border border-[#eee7c9] bg-[#fffef8] p-5">

        <p className="whitespace-pre-wrap leading-7 text-neutral-700">
          {result.answer}
        </p>

      </div>

    </section>
  );
}