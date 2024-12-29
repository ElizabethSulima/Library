from contextlib import asynccontextmanager

from core.dependency import async_engine
from fastapi import FastAPI
from models.base import Base

from api.author import author_router
from api.book import book_router
from api.borrow import borrow_router


@asynccontextmanager
async def lifespan(application: FastAPI):  # pylint:disable=W0613
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await async_engine.dispose()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(author_router)
app.include_router(book_router)
app.include_router(borrow_router)
