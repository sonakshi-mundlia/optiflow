from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis.asyncio import Redis

from .config import settings
from .db import engine
from .init_db import init_db
from .routes.query_route import router as query_router
from . import redis_client as redis_state


@asynccontextmanager
async def lifespan(app: FastAPI):

    # ---------------------------------------------------------
    # DATABASE
    # ---------------------------------------------------------

    await init_db()

    # ---------------------------------------------------------
    # REDIS
    # ---------------------------------------------------------

    redis_state.redis_client = Redis.from_url(
        settings.REDIS_URL,
        decode_responses=True,
    )

    yield

    # ---------------------------------------------------------
    # SHUTDOWN
    # ---------------------------------------------------------

    if redis_state.redis_client is not None:
        await redis_state.redis_client.close()

    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(query_router)


@app.get("/")
async def root():

    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }