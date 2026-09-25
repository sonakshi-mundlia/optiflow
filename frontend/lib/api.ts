const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export type QueryResult = {
  request_id: string;
  query: string;
  answer: string;

  route: string;
  model: string;
  complexity: string;
  router_score: number;

  cache_hit: boolean;
  cache_type: string | null;
  similarity: number | null;

  input_tokens: number;
  output_tokens: number;

  estimated_cost: number;
  latency_ms: number;
  quality_score: number;
};


export async function processQuery(
  query: string
): Promise<QueryResult> {

  const response = await fetch(
    `${API_URL}/query/`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        query,
      }),
    }
  );


  if (!response.ok) {

    const errorText = await response.text();

    throw new Error(
      errorText || "Failed to process query"
    );
  }


  return response.json();
}


export async function getHistory() {

  const response = await fetch(
    `${API_URL}/query/history`,
    {
      cache: "no-store",
    }
  );


  if (!response.ok) {
    throw new Error(
      "Failed to load query history"
    );
  }


  return response.json();
}