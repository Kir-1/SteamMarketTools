from typing import Any, Callable, Set
from pathlib import Path, PosixPath
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, RedisDsn
from redis import asyncio as aioredis


class Settings(BaseSettings):
    BASE_DIR: PosixPath = Path(__file__).resolve().parent.parent
    DEBUG: bool
    APP_TITLE: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    REDIS_HOST: str

    @property
    def DATABASE_URL(self):
        return PostgresDsn(
            url=f"postgresql+asyncpg://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@db:5432/{self.DATABASE_NAME}"
        )

    @property
    def PWD_CONTEXT(self):
        return CryptContext(schemes=["bcrypt"], deprecated="auto")

    @property
    def OAUTH2_BEARER(self):
        return OAuth2PasswordBearer(tokenUrl="auth/users/token")

    @property
    def REDIS(self):
        return aioredis.StrictRedis(host=self.REDIS_HOST)

    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env")


settings = Settings()
