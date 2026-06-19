import asyncio
import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool

sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Импортируем Base и асинхронный engine из твоей базы данных
from src.infrastructure.sqlite.database import Base, engine, ASYNC_DATABASE_URL

# Импорт моделей для поддержки autogenerate
from src.infrastructure.sqlite.models.users import User
from src.infrastructure.sqlite.models.posts import Post
from src.infrastructure.sqlite.models.post_image import PostImage
from src.infrastructure.sqlite.models.category import Category
from src.infrastructure.sqlite.models.comment import Comment
from src.infrastructure.sqlite.models.location import Location

target_metadata = Base.metadata

# Устанавливаем асинхронный URL
config.set_main_option("sqlalchemy.url", ASYNC_DATABASE_URL)


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# Вспомогательная функция для запуска миграций внутри асинхронного соединения
def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Запуск миграций в асинхронном режиме"""
    # Используем твой готовый асинхронный движок напрямую
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    # Запускаем асинхронный цикл для выполнения миграций онлайн
    asyncio.run(run_migrations_online())