import time
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from ..models.query_model import QueryLog
from ..schemas.query_schema import QueryRequest

from .complexity_service import ComplexityService
from .cost_service import CostService
from .quality_service import estimate_quality
from .routing.routing_service import RoutingService
from .inference.inference_service import InferenceService
from .inference.model_registry import ModelRegistry
from .cache.cache_service import SemanticCacheService


class QueryService:

    def __init__(
        self,
        redis: Redis,
    ):

        # -----------------------------------------------------
        # ONE MODEL REGISTRY
        # -----------------------------------------------------

        self.model_registry = ModelRegistry()

        # -----------------------------------------------------
        # SERVICES
        # -----------------------------------------------------

        self.complexity_service = (
            ComplexityService()
        )

        self.routing_service = RoutingService(
            self.model_registry
        )

        self.inference = InferenceService(
            self.model_registry
        )

        self.cache = SemanticCacheService(
            redis,
            self.model_registry,
        )

        self.cost_service = CostService()

    async def process(
        self,
        data: QueryRequest,
        db: AsyncSession,
    ):

        total_start = time.perf_counter()

        request_id = str(
            uuid.uuid4()
        )

        # =====================================================
        # 1. COMPLEXITY
        # =====================================================

        complexity, router_score = (
            self.complexity_service.analyze(
                data.query
            )
        )

        # =====================================================
        # 2. SEMANTIC CACHE
        # =====================================================

        cached = await self.cache.get(
            data.query
        )

        if cached:

            answer = cached["answer"]

            model = cached.get(
                "model",
                "cache",
            )

            route = "semantic_cache"

            cache_hit = True

            cache_type = "semantic"

            similarity = round(
                cached["similarity"],
                4,
            )

            input_tokens = 0
            output_tokens = 0

            estimated_cost = 0.0

        else:

            # =================================================
            # 3. SELECT MODEL
            # =================================================

            selected_model = (
                self.routing_service.select_model(
                    complexity,
                    router_score,
                )
            )

            print(
                f"Router selected: "
                f"{selected_model}"
            )

            # =================================================
            # 4. GENERATE ANSWER
            # =================================================

            generated = await self.inference.generate(
                data.query,
                selected_model,
            )

            answer = generated["answer"]

            model = generated["model"]

            input_tokens = (
                generated["input_tokens"]
            )

            output_tokens = (
                generated["output_tokens"]
            )

            # =================================================
            # 5. ROUTE
            # =================================================

            route = "gemini_llm"

            cache_hit = False

            cache_type = None

            similarity = None

            # =================================================
            # 6. COST
            # =================================================

            estimated_cost = (
                self.cost_service.calculate(
                    model=model,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                )
            )

            # =================================================
            # 7. STORE IN CACHE
            # =================================================

            await self.cache.set(
                data.query,
                answer,
                model,
            )

        # =====================================================
        # 8. TOTAL LATENCY
        # =====================================================

        total_latency = (
            time.perf_counter()
            - total_start
        ) * 1000

        # =====================================================
        # 9. QUALITY
        # =====================================================

        quality = estimate_quality(
            data.query,
            answer,
        )

        # =====================================================
        # 10. DATABASE
        # =====================================================

        row = QueryLog(
            request_id=request_id,
            query=data.query,
            answer=answer,
            route=route,
            model=model,
            complexity=complexity,
            router_score=router_score,
            cache_hit=cache_hit,
            cache_type=cache_type,
            similarity=similarity,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            estimated_cost=estimated_cost,
            latency_ms=total_latency,
            quality_score=quality,
        )

        db.add(row)

        await db.commit()

        # =====================================================
        # 11. RESPONSE
        # =====================================================

        return {
            "request_id": request_id,
            "query": data.query,
            "answer": answer,
            "route": route,
            "model": model,
            "complexity": complexity,
            "router_score": router_score,
            "cache_hit": cache_hit,
            "cache_type": cache_type,
            "similarity": similarity,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "estimated_cost": estimated_cost,
            "latency_ms": total_latency,
            "quality_score": quality,
        }


    async def history(
        self,
        db: AsyncSession,
        limit: int = 20,
    ):
        result = await db.execute(
            select(QueryLog)
            .order_by(QueryLog.created_at.desc())
            .limit(limit)
        )

        rows = result.scalars().all()

        return [
            {
                "request_id": row.request_id,
                "query": row.query,
                "answer": row.answer,
                "route": row.route,
                "model": row.model,
                "complexity": row.complexity,
                "router_score": row.router_score,
                "cache_hit": row.cache_hit,
                "cache_type": row.cache_type,
                "similarity": row.similarity,
                "input_tokens": row.input_tokens,
                "output_tokens": row.output_tokens,
                "estimated_cost": row.estimated_cost,
                "latency_ms": row.latency_ms,
                "quality_score": row.quality_score,
                "created_at": row.created_at.isoformat()
                if row.created_at
                else None,
            }
            for row in rows
        ]