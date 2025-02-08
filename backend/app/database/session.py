from typing import AsyncGenerator
from app.core.config import settings
from sqlalchemy.ext.asyncio import (
    AsyncSession, create_async_engine, async_sessionmaker
)


async_engine = create_async_engine(settings.db_url, echo=settings.app_debug)
async_session = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
    future=True
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
