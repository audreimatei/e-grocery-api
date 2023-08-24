from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

from src.config import cfg

async_engine = create_async_engine(
    url=cfg.DB_URL,
    pool_size=cfg.POOL_SIZE,
    max_overflow=cfg.MAX_OVERFLOW,
    pool_timeout=cfg.POOL_TIMEOUT,
    pool_pre_ping=True
)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    autoflush=True,
    expire_on_commit=False
)


async def get_engine_and_sessionmaker(
    db_url: str
) -> tuple[AsyncEngine, async_sessionmaker[AsyncSession]]:

    async_engine = create_async_engine(
        url=db_url,
        pool_size=cfg.POOL_SIZE,
        max_overflow=cfg.MAX_OVERFLOW,
        pool_timeout=cfg.POOL_TIMEOUT,
        pool_pre_ping=True
    )
    AsyncSessionLocal = async_sessionmaker(
        bind=async_engine,
        autoflush=True,
        expire_on_commit=False
    )

    return async_engine, AsyncSessionLocal
