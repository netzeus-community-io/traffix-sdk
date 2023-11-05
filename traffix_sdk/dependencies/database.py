from collections.abc import AsyncGenerator
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from traffix_sdk.config import settings
from traffix_sdk.database.async_session import SessionLocal, engine


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Returns an Async Session"""
    async with SessionLocal() as session:
        yield session


async def init_db() -> None:
    """Creates all database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
