from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.config import settings


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


async def get_db() -> AsyncGenerator[AsyncSession, None, None]:
    """
    Зависимость для получения сессии базы данных.
    """
    async with AsyncSessionFactory() as session:
        yield session
