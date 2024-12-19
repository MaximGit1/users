import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy import pool
from alembic import context
from auth_service.infrastructure.database.models import metadata

# Загружаем переменные окружения из .env
load_dotenv()

# Загружаем конфигурацию Alembic
config = context.config

# Указываем метаданные модели для автогенерации миграций
target_metadata = metadata


def run_migrations_offline() -> None:
    """Запуск миграций в режиме 'offline'."""
    url = os.getenv("SQLALCHEMY_URL")  # Читаем URL из .env
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    """Настройка и выполнение миграций."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Запуск миграций в режиме 'online'."""
    connectable: AsyncEngine = create_async_engine(
        os.getenv("SQLALCHEMY_URL"),  # Асинхронный движок
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio

    asyncio.run(run_migrations_online())
