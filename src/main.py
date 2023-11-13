from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.config import settings
from src.auth import router as auth_router
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    yield
    await settings.REDIS.close()
    # Clean up the ML models and release the resources


def create_app():
    app = FastAPI(
        debug=settings.DEBUG, title=f"{settings.APP_TITLE}", lifespan=lifespan
    )

    app.include_router(router=auth_router, prefix="/auth")
    return app


if __name__ == "__main__":
    uvicorn.run(create_app(), host="0.0.0.0", port=8000)
