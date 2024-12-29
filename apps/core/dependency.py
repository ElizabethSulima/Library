from typing import Annotated, AsyncIterator

from core.settings import config
from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


async_engine = create_async_engine(config.async_dsn)  # type: ignore
async_session = async_sessionmaker(async_engine)


async def get_async_session() -> AsyncIterator[AsyncSession]:
    # pylint: disable=C0301
    async with async_session() as session:
        yield session


AsyncSessionDepency = Annotated[
    AsyncSession, Depends(get_async_session, use_cache=True)
]
