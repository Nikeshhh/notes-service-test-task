# Source: https://github.com/grillazz/fastapi-sqlalchemy-asyncpg/blob/main/alembic/env.py

import asyncio

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

from src.config import settings
from src.database.models import Base


target_metadata = Base.metadata


def do_run_migrations(connection):
    """
    Непосредственно запускает миграции.
    """
    context.configure(
        compare_type=True,
        dialect_opts={"paramstyle": "named"},
        connection=connection,
        target_metadata=target_metadata,
        include_schemas=True,
        # literal_binds=True,
        version_table_schema=target_metadata.schema,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_async():
    """
    Запускает миграции через асинхронное подключение.
    """
    connectable = create_async_engine(
        settings.postgres_url.unicode_string(), future=True
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


asyncio.run(run_migrations_async())