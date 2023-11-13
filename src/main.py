from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.config import settings
from src.auth import router as auth_router
import uvicorn

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    redis = aioredis.from_url(
        "redis://localhost", encoding="utf8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield
    # Clean up the ML models and release the resources
    redis.flushall()


def create_app():
    app = FastAPI(
        debug=settings.DEBUG, title=f"{settings.APP_TITLE}", lifespan=lifespan
    )

    app.include_router(router=auth_router, prefix="/auth")
    return app


if __name__ == "__main__":
    uvicorn.run(create_app(), host="0.0.0.0", port=8000)
