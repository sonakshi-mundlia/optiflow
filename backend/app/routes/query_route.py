from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from redis.asyncio import Redis

from ..db import get_db

from ..schemas.query_schema import (
    QueryRequest,
    QueryResponse
)

from ..services.query_service import (
    QueryService
)

from ..redis_client import (
    get_redis
)


router = APIRouter(
    prefix="/query",
    tags=["Query"]
)


@router.post(
    "/",
    response_model=QueryResponse
)
async def process_query(

    request: QueryRequest,

    db: AsyncSession = Depends(
        get_db
    ),

    redis: Redis = Depends(
        get_redis
    )
):

    service = QueryService(
        redis
    )

    return await service.process(
        request,
        db
    )


@router.get(
    "/history"
)
async def query_history(

    db: AsyncSession = Depends(
        get_db
    )
):

    service = QueryService.__new__(
        QueryService
    )

    return await service.history(
        db
    )