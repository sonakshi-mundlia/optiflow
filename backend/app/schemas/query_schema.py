from pydantic import BaseModel, Field


class QueryRequest(BaseModel):

    query: str = Field(
        min_length=1,
        max_length=10000
    )


class QueryResponse(BaseModel):

    request_id: str

    query: str

    answer: str

    route: str

    model: str

    complexity: str

    router_score: float

    cache_hit: bool

    cache_type: str | None = None

    similarity: float | None = None

    input_tokens: int

    output_tokens: int

    estimated_cost: float

    latency_ms: float

    quality_score: float