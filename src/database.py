from typing import Generator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)
from asyncio import current_task
from src.config import settings


class Database:
    instance = None

    def __new__(cls):
        if not Database.instance:
            Database.instance = super().__new__(cls)
            Database.instance.engine = create_async_engine(
                url=settings.DATABASE_URL.unicode_string(), echo=False
            )
            Database.instance.session_factory = async_sessionmaker(
                bind=Database.instance.engine,
                autoflush=False,
                autocommit=False,
                expire_on_commit=False,
            )
        return Database.instance

    async def get_async_session(self) -> Generator:
        scope_session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        yield scope_session
        await scope_session.close()


class TestDatabase:
    instance = None

    def __new__(cls):
        if not Database.instance:
            Database.instance = super().__new__(cls)
            Database.instance.engine = create_async_engine(
                url=settings.TEST_DATABASE_URL.unicode_string(), echo=False
            )
            Database.instance.session_factory = async_sessionmaker(
                bind=Database.instance.engine,
                autoflush=False,
                autocommit=False,
                expire_on_commit=False,
            )
        return Database.instance

    async def get_async_session(self) -> Generator:
        scope_session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        yield scope_session
        await scope_session.close()


database = Database()

test_database = TestDatabase()
