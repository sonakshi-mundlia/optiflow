from redis.asyncio import Redis

from .config import settings


redis_client: Redis | None = None


def get_redis() -> Redis:

    if redis_client is None:
        raise RuntimeError(
            "Redis has not been initialized"
        )

    return redis_client