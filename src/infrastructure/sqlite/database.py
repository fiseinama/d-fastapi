from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from src.core.config import settings


def get_async_database_url(url: str) -> str:
    if url.startswith("sqlite+aiosqlite") or url.startswith("postgresql+asyncpg"):
        return url
    if url.startswith("sqlite://"):
        return url.replace("sqlite://", "sqlite+aiosqlite://", 1)
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    raise ValueError(f"Unsupported DATABASE_URL: {url}")


def get_sync_database_url(url: str) -> str:
    if url.startswith("sqlite+aiosqlite"):
        return url.replace("sqlite+aiosqlite", "sqlite", 1)
    if url.startswith("postgresql+asyncpg"):
        return url.replace("postgresql+asyncpg", "postgresql", 1)
    return url


ASYNC_DATABASE_URL = get_async_database_url(settings.DATABASE_URL)
SYNC_DATABASE_URL = get_sync_database_url(ASYNC_DATABASE_URL)

connect_args = {}
if ASYNC_DATABASE_URL.startswith("sqlite+aiosqlite"):
    connect_args = {"check_same_thread": False}

# Настраиваем аргументы для движка базы данных
engine_kwargs = {
    "connect_args": connect_args
}

if ASYNC_DATABASE_URL.startswith("postgresql+asyncpg"):
    engine_kwargs.update({
        "pool_size": 50,         # Открываем 50 постоянных труб к Postgres
        "max_overflow": 30,      # Разрешаем создавать ещё 30 в пиковые моменты
        "pool_timeout": 30       # Ждём освобождения трубы 30 секунд
    })

# Создаём сам движок с нашими настройками
engine = create_async_engine(
    ASYNC_DATABASE_URL,
    **engine_kwargs
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

Base = declarative_base()
