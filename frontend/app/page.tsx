import Link from "next/link";

const features = [
  {
    title: "Smart Routing",
    description:
      "Analyze query complexity and choose an appropriate inference path.",
    color: "yellow",
  },
  {
    title: "Semantic Cache",
    description:
      "Reuse responses when a sufficiently similar query already exists.",
    color: "green",
  },
  {
    title: "Cost-Aware Inference",
    description:
      "Use different inference paths depending on the needs of the query.",
    color: "blue",
  },
  {
    title: "Execution Insights",
    description:
      "Track route, model, latency, cost, tokens, and response quality.",
    color: "red",
  },
];

const steps = [
  ["01", "Analyze", "Estimate query complexity.", "yellow"],
  ["02", "Cache", "Check for a similar request.", "green"],
  ["03", "Route", "Select the inference path.", "blue"],
  ["04", "Measure", "Track execution metrics.", "red"],
];

function stepClass(color: string) {
  if (color === "green") {
    return "green-text";
  }

  if (color === "blue") {
    return "blue-text";
  }

  if (color === "red") {
    return "red-text";
  }

  return "brand";
}

export default function Home() {
  return (
    <main className="min-h-screen bg-white text-[var(--text)]">

      {/* HEADER */}

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
                Intelligent AI Query Routing
              </div>
            </div>
          </Link>

          <Link
            href="/query"
            className="btn-blue"
          >
            Try Now
          </Link>

        </div>
      </header>


      {/* HERO */}

      <section className="border-b border-[var(--border)]">

        <div className="mx-auto max-w-6xl px-5 py-16 lg:px-8 lg:py-20">

          <div className="max-w-4xl">

            <span className="badge-yellow">
              Intelligent AI Query Routing
            </span>

            <h1 className="mt-6 font-black tracking-tight text-3xl lg:text-4xl">
              The right model
              <span className="mt-1 block text-5xl lg:text-6xl">
                for every query.
              </span>
            </h1>

            <p className="mt-6 max-w-2xl text-lg leading-8 muted">
              OptiFlow analyzes a query, checks semantic cache, selects an
              inference path, and measures the execution.
            </p>

            <div className="mt-8 flex flex-wrap gap-3">

              <Link
                href="/query"
                className="btn-blue"
              >
                Try Now →
              </Link>

              <a
                href="#how-it-works"
                className="rounded-lg border border-[var(--border)] bg-white px-5 py-3 text-sm font-semibold hover-yellow"
              >
                How It Works
              </a>

            </div>

          </div>


          {/* SIMPLE PIPELINE */}

          <div className="card mt-16 p-6">

            <div className="accent" />

            <p className="mt-4 text-xs font-bold uppercase tracking-widest brand">
              OptiFlow Pipeline
            </p>

            <h2 className="mt-2 text-2xl font-bold">
              Query → Decision → Answer
            </h2>


            <div className="mt-7 grid gap-4 md:grid-cols-4">

              {steps.map(
                ([number, title, description, color]) => (
                  <div
                    key={number}
                    className="card hover-yellow p-5"
                  >

                    <div
                      className={`text-sm font-black ${stepClass(
                        color
                      )}`}
                    >
                      {number}
                    </div>

                    <h3 className="mt-2 font-bold">
                      {title}
                    </h3>

                    <p className="mt-2 text-sm leading-6 muted">
                      {description}
                    </p>

                  </div>
                )
              )}

            </div>

          </div>

        </div>
      </section>


      {/* WHAT IS OPTIFLOW */}

      <section className="surface border-b border-[var(--border)]">

        <div className="mx-auto max-w-6xl px-5 py-20 lg:px-8">

          <div className="max-w-3xl">

            <div className="accent" />

            <p className="mt-4 text-xs font-bold uppercase tracking-widest brand">
              What is OptiFlow?
            </p>

            <h2 className="mt-3 text-3xl font-black sm:text-4xl">
              Intelligent routing for AI inference.
            </h2>

            <p className="mt-5 leading-8 muted">
              Different queries can require different amounts of computation.
              OptiFlow evaluates the request, checks for reusable responses,
              and chooses an appropriate execution path.
            </p>

          </div>

        </div>

      </section>


      {/* FEATURES */}

      <section className="border-b border-[var(--border)]">

        <div className="mx-auto max-w-6xl px-5 py-20 lg:px-8">

          <div className="accent" />

          <p className="mt-4 text-xs font-bold uppercase tracking-widest brand">
            Core Features
          </p>

          <h2 className="mt-3 text-3xl font-black sm:text-4xl">
            What OptiFlow does
          </h2>


          <div className="mt-10 grid gap-5 md:grid-cols-2">

            {features.map((feature) => {

              const accentClass =
                feature.color === "green"
                  ? "bg-[var(--green)]"
                  : feature.color === "blue"
                    ? "bg-[var(--blue)]"
                    : feature.color === "red"
                      ? "bg-[var(--red)]"
                      : "bg-[var(--yellow)]";

              return (
                <div
                  key={feature.title}
                  className="card hover-yellow p-6"
                >

                  <div
                    className={`h-1.5 w-10 rounded-full ${accentClass}`}
                  />

                  <h3 className="mt-5 text-lg font-bold">
                    {feature.title}
                  </h3>

                  <p className="mt-3 text-sm leading-7 muted">
                    {feature.description}
                  </p>

                </div>
              );
            })}

          </div>

        </div>
      </section>


      {/* HOW IT WORKS */}

      <section
        id="how-it-works"
        className="surface border-b border-[var(--border)]"
      >

        <div className="mx-auto max-w-6xl px-5 py-20 lg:px-8">

          <div className="accent" />

          <p className="mt-4 text-xs font-bold uppercase tracking-widest brand">
            How It Works
          </p>

          <h2 className="mt-3 text-3xl font-black sm:text-4xl">
            Four simple stages.
          </h2>


          <div className="mt-10 grid gap-4 md:grid-cols-2">

            {steps.map(
              ([number, title, description, color]) => (
                <div
                  key={number}
                  className="card flex items-center gap-4 p-5"
                >

                  <div
                    className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-lg ${
                      color === "green"
                        ? "green-light"
                        : color === "blue"
                          ? "blue-light"
                          : color === "red"
                            ? "red-light"
                            : "brand-light"
                    }`}
                  >
                    <span
                      className={`font-black ${stepClass(
                        color
                      )}`}
                    >
                      {number}
                    </span>
                  </div>


                  <div>

                    <h3 className="font-bold">
                      {title}
                    </h3>

                    <p className="mt-1 text-sm muted">
                      {description}
                    </p>

                  </div>

                </div>
              )
            )}

          </div>

        </div>

      </section>


      {/* EXECUTION INSIGHTS */}

      <section className="border-b border-[var(--border)]">

        <div className="mx-auto max-w-6xl px-5 py-20 lg:px-8">

          <div className="grid gap-10 lg:grid-cols-2 lg:items-center">

            <div>

              <div className="accent" />

              <p className="mt-4 text-xs font-bold uppercase tracking-widest brand">
                Execution Insights
              </p>

              <h2 className="mt-3 text-3xl font-black sm:text-4xl">
                See what happened behind the answer.
              </h2>

              <p className="mt-5 leading-8 muted">
                After processing a query, OptiFlow shows useful execution
                information without exposing raw internal logs.
              </p>

            </div>


            <div className="grid grid-cols-2 gap-3">

              {[
                ["Complexity", "yellow"],
                ["Route", "blue"],
                ["Model", "blue"],
                ["Cache", "green"],
                ["Similarity", "yellow"],
                ["Latency", "yellow"],
                ["Estimated Cost", "blue"],
                ["Token Usage", "red"],
              ].map(([item, color]) => (

                <div
                  key={item}
                  className="card p-4"
                >

                  <div className="text-sm font-bold">
                    {item}
                  </div>

                  <div
                    className={`mt-2 h-1 w-7 rounded-full ${
                      color === "green"
                        ? "bg-[var(--green)]"
                        : color === "blue"
                          ? "bg-[var(--blue)]"
                          : color === "red"
                            ? "bg-[var(--red)]"
                            : "bg-[var(--yellow)]"
                    }`}
                  />

                </div>

              ))}

            </div>

          </div>

        </div>

      </section>


      {/* FINAL CTA */}

      <section>

        <div className="mx-auto max-w-4xl px-5 py-24 text-center lg:px-8">

          <div className="card brand-border p-10 sm:p-14">

            <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-xl brand-bg font-black">
              O
            </div>

            <h2 className="mt-6 text-3xl font-black sm:text-4xl">
              Ready to try OptiFlow?
            </h2>

            <p className="mx-auto mt-4 max-w-xl muted">
              Enter a query and see how OptiFlow analyzes, routes, caches,
              and measures the request.
            </p>

            <Link
              href="/query"
              className="btn-blue mt-7"
            >
              Try Now →
            </Link>

          </div>

        </div>

      </section>


      <footer className="border-t border-[var(--border)] py-6 text-center text-xs muted">
        OptiFlow • Intelligent AI Query Routing
      </footer>

    </main>
  );
}