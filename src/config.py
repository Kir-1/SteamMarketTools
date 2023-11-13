from typing import Any, Callable, Set
from pathlib import Path, PosixPath
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, AnyUrl


class Settings(BaseSettings):
    BASE_DIR: PosixPath = Path(__file__).resolve().parent.parent
    DATABASE_URL: PostgresDsn
    DEBUG: bool
    APP_TITLE: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    PORT: int
    SECRET_KEY: str
    ALGORITHM: str

    @property
    def PWD_CONTEXT(self):
        return CryptContext(schemes=["bcrypt"], deprecated="auto")

    @property
    def OAUTH2_BEARER(self):
        return OAuth2PasswordBearer(tokenUrl="auth/users/token")

    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env")


settings = Settings()
