from datetime import datetime

from sqlalchemy import (
    String,
    Text,
    DateTime,
    Float,
    Integer,
    Boolean
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from ..db import Base


class QueryLog(Base):

    __tablename__ = "query_logs"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    request_id: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True
    )

    query: Mapped[str] = mapped_column(
        Text
    )

    answer: Mapped[str] = mapped_column(
        Text
    )

    # Routing information

    route: Mapped[str] = mapped_column(
        String(32)
    )

    model: Mapped[str] = mapped_column(
        String(128)
    )

    complexity: Mapped[str] = mapped_column(
        String(32)
    )

    router_score: Mapped[float] = mapped_column(
        Float
    )

    # Cache information

    cache_hit: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    cache_type: Mapped[str | None] = mapped_column(
        String(32),
        nullable=True
    )

    similarity: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    # Token information

    input_tokens: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    output_tokens: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    # Metrics

    estimated_cost: Mapped[float] = mapped_column(
        Float,
        default=0.0
    )

    latency_ms: Mapped[float] = mapped_column(
        Float,
        default=0.0
    )

    quality_score: Mapped[float] = mapped_column(
        Float,
        default=0.0
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )