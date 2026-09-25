import hashlib
import json
import math
import time

from redis.asyncio import Redis

from ..embedding_service import EmbeddingService
from ..inference.model_registry import ModelRegistry
from ...config import settings


class SemanticCacheService:

    CACHE_PREFIX = "optiflow:semantic:entry:"
    CACHE_INDEX = "optiflow:semantic:index"

    def __init__(
        self,
        redis: Redis,
        model_registry: ModelRegistry,
    ):

        self.redis = redis

        self.embedding_service = EmbeddingService(
            model_registry
        )

        self.threshold = (
            settings.SEMANTIC_CACHE_THRESHOLD
        )

        self.max_entries = (
            settings.MAX_CACHE_ENTRIES
        )

    # =========================================================
    # CREATE CACHE KEY
    # =========================================================

    def _create_key(
        self,
        query: str,
    ) -> str:

        normalized_query = (
            query.strip()
            .lower()
        )

        query_hash = hashlib.sha256(
            normalized_query.encode("utf-8")
        ).hexdigest()

        return (
            f"{self.CACHE_PREFIX}"
            f"{query_hash}"
        )

    # =========================================================
    # COSINE SIMILARITY
    # =========================================================

    def _cosine_similarity(
        self,
        vector_a: list[float],
        vector_b: list[float],
    ) -> float:

        if not vector_a or not vector_b:
            return 0.0

        if len(vector_a) != len(vector_b):
            return 0.0

        dot_product = sum(
            a * b
            for a, b in zip(
                vector_a,
                vector_b,
            )
        )

        magnitude_a = math.sqrt(
            sum(
                a * a
                for a in vector_a
            )
        )

        magnitude_b = math.sqrt(
            sum(
                b * b
                for b in vector_b
            )
        )

        if magnitude_a == 0 or magnitude_b == 0:
            return 0.0

        return (
            dot_product
            / (magnitude_a * magnitude_b)
        )

    # =========================================================
    # GET FROM CACHE
    # =========================================================

    async def get(
        self,
        query: str,
    ):

        query = query.strip()

        if not query:
            return None

        # -----------------------------------------------------
        # STEP 1: EXACT QUERY CACHE
        # -----------------------------------------------------

        exact_key = self._create_key(query)

        exact_cached = await self.redis.get(
            exact_key
        )

        if exact_cached:

            try:

                data = json.loads(
                    exact_cached
                )

                data["similarity"] = 1.0

                print(
                    "CACHE HIT: exact query"
                )

                return data

            except json.JSONDecodeError:

                print(
                    "Invalid cache data found. "
                    "Deleting cache entry."
                )

                await self.redis.delete(
                    exact_key
                )

        # -----------------------------------------------------
        # STEP 2: CREATE QUERY EMBEDDING
        # -----------------------------------------------------

        try:

            query_embedding = (
                await self.embedding_service.embed(
                    query
                )
            )

        except Exception as error:

            print(
                "Embedding failed during "
                "cache lookup."
            )

            print(error)

            # Cache failure should NOT stop
            # the actual LLM request.
            return None

        # -----------------------------------------------------
        # STEP 3: SEARCH REDIS CACHE
        # -----------------------------------------------------

        best_match = None
        best_similarity = 0.0

        async for key in self.redis.scan_iter(
            match=f"{self.CACHE_PREFIX}*"
        ):

            try:

                cached_data = await self.redis.get(
                    key
                )

                if not cached_data:
                    continue

                data = json.loads(
                    cached_data
                )

                cached_embedding = data.get(
                    "embedding"
                )

                if not cached_embedding:
                    continue

                similarity = (
                    self._cosine_similarity(
                        query_embedding,
                        cached_embedding,
                    )
                )

                if similarity > best_similarity:

                    best_similarity = similarity

                    best_match = data

            except (
                json.JSONDecodeError,
                TypeError,
                ValueError,
            ) as error:

                print(
                    f"Invalid cache entry: "
                    f"{key}"
                )

                print(error)

                continue

        # -----------------------------------------------------
        # STEP 4: CHECK THRESHOLD
        # -----------------------------------------------------

        if (
            best_match is not None
            and best_similarity >= self.threshold
        ):

            best_match["similarity"] = round(
                best_similarity,
                4,
            )

            print(
                "CACHE HIT: semantic"
            )

            print(
                f"Similarity: "
                f"{best_similarity:.4f}"
            )

            print(
                f"Threshold: "
                f"{self.threshold}"
            )

            return best_match

        # -----------------------------------------------------
        # CACHE MISS
        # -----------------------------------------------------

        print(
            "CACHE MISS"
        )

        print(
            f"Best similarity: "
            f"{best_similarity:.4f}"
        )

        print(
            f"Threshold: "
            f"{self.threshold}"
        )

        return None

    # =========================================================
    # SAVE TO CACHE
    # =========================================================

    async def set(
        self,
        query: str,
        answer: str,
        model: str,
    ):

        query = query.strip()

        if not query or not answer:
            return

        # -----------------------------------------------------
        # CREATE EMBEDDING
        # -----------------------------------------------------

        try:

            embedding = (
                await self.embedding_service.embed(
                    query
                )
            )

        except Exception as error:

            print(
                "Embedding failed while "
                "saving cache."
            )

            print(error)

            # Do not make a successful
            # LLM request fail just because
            # cache storage failed.
            return

        # -----------------------------------------------------
        # CREATE CACHE DATA
        # -----------------------------------------------------

        cache_key = self._create_key(
            query
        )

        cache_data = {
            "query": query,
            "answer": answer,
            "model": model,
            "embedding": embedding,
            "created_at": time.time(),
        }

        # -----------------------------------------------------
        # SAVE ENTRY
        # -----------------------------------------------------

        await self.redis.set(
            cache_key,
            json.dumps(cache_data),
        )

        # -----------------------------------------------------
        # ADD ENTRY TO TIMESTAMP INDEX
        # -----------------------------------------------------

        await self.redis.zadd(
            self.CACHE_INDEX,
            {
                cache_key: time.time()
            },
        )

        print(
            f"CACHE SAVED: {cache_key}"
        )

        # -----------------------------------------------------
        # ENFORCE MAX CACHE SIZE
        # -----------------------------------------------------

        cache_count = await self.redis.zcard(
            self.CACHE_INDEX
        )

        if cache_count <= self.max_entries:
            return

        number_to_remove = (
            cache_count
            - self.max_entries
        )

        oldest_keys = await self.redis.zrange(
            self.CACHE_INDEX,
            0,
            number_to_remove - 1,
        )

        if not oldest_keys:
            return

        # Delete actual Redis entries
        await self.redis.delete(
            *oldest_keys
        )

        # Remove them from timestamp index
        await self.redis.zrem(
            self.CACHE_INDEX,
            *oldest_keys
        )

        print(
            f"Removed {len(oldest_keys)} "
            f"old cache entries."
        )