from collections.abc import AsyncGenerator
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine,
)
from sqlalchemy import delete
import pytest

from tests.fixtures import *  # noqa: F403

from src.database.connection import get_db
from src.auth.models import User  # noqa: F401
from src.notes.models import Note  # noqa: F401
from src.database.models import Base
from src.main import app
from src.config import settings


# Использование тестовой базы данных
settings.POSTGRES_DB = "testdb"
async_engine = create_async_engine(
    settings.postgres_url.unicode_string(),
    future=True,  # Для использования движка из SQLAlchemy 2.x
    echo=True,  # Для вывода логов в консоль
)

AsyncSessionFactory = async_sessionmaker(
    async_engine,
    autoflush=False,  # Отключить автоматическую синхронизацию изменений
    expire_on_commit=False,  # Отключить очистку объектов после коммита
)


@pytest.fixture(scope="session")
async def async_db_engine() -> AsyncGenerator[AsyncEngine, None, None]:
    """
    Обеспечивает создание таблиц перед тестами и удаление после тестов.
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield async_engine

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def async_db(
    async_db_engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None, None]:
    """
    Обеспечивает откат изменений в базе данных после каждого теста для обеспечения изоляции.
    """
    async with AsyncSessionFactory() as session:
        await session.begin()

        yield session

        await session.rollback()

        for table in reversed(Base.metadata.sorted_tables):
            stmt = delete(table)
            await session.execute(stmt)
            await session.commit()


@pytest.fixture
async def async_client(
    async_db: AsyncSession,
) -> AsyncGenerator[AsyncClient, None, None]:
    """
    Предоставляет асинхронный HTTP-клиент для тестирования.
    """

    def override_get_db():
        yield async_db

    app.dependency_overrides[get_db] = override_get_db
    yield AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    del app.dependency_overrides[get_db]


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"
