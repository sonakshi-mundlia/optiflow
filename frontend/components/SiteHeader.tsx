import Link from "next/link";

export default function SiteHeader() {
  return (
    <header className="border-b border-[#E8DFC3] bg-white">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-5 py-4 lg:px-8">

        <Link
          href="/"
          className="flex items-center gap-3"
        >
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-[#D4A928] font-black text-white">
            O
          </div>

          <div>
            <div className="font-bold text-[#202124]">
              OptiFlow
            </div>

            <div className="text-xs text-[#7A766B]">
              AI Query Routing
            </div>
          </div>
        </Link>

        <Link
          href="/query"
          className="rounded-lg bg-[#4285F4] px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-[#3367D6]"
        >
          Try Now
        </Link>

      </div>
    </header>
  );
}