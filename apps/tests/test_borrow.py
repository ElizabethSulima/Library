from typing import Sequence

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from tests import factory as data_factory


pytestmark = pytest.mark.anyio


async def test_get_borrows(
    client: AsyncClient,
    factory: data_factory.FactoryCallback,
    async_session: AsyncSession,
):
    author = await factory(data_factory.AuthorFactory)
    assert not isinstance(author, Sequence)
    await async_session.refresh(author)

    book = await factory(data_factory.BookFactory, author_id=author.id)
    assert not isinstance(book, Sequence)
    await async_session.refresh(book)

    await factory(data_factory.BorrowFactory, 10, book_id=book.id)
    response = await client.get("/borrows/")
    assert response.status_code == status.HTTP_200_OK


async def test_get_borrow_id(
    client: AsyncClient,
    factory: data_factory.FactoryCallback,
    async_session: AsyncSession,
):
    author = await factory(data_factory.AuthorFactory)
    assert not isinstance(author, Sequence)
    await async_session.refresh(author)

    book = await factory(data_factory.BookFactory, author_id=author.id)
    assert not isinstance(book, Sequence)
    await async_session.refresh(book)

    borrow = await factory(data_factory.BorrowFactory, book_id=book.id)
    assert not isinstance(borrow, Sequence)
    await async_session.refresh(borrow)

    response = await client.get(f"/borrows/{borrow.id}/")
    assert response.status_code == status.HTTP_200_OK


async def test_create_borrow(
    client: AsyncClient,
    factory: data_factory.FactoryCallback,
    async_session: AsyncSession,
):
    author = await factory(data_factory.AuthorFactory)
    assert not isinstance(author, Sequence)
    await async_session.refresh(author)

    book = await factory(data_factory.BookFactory, author_id=author.id)
    assert not isinstance(book, Sequence)
    await async_session.refresh(book)

    data = {
        "reader_name": "Sanita",
        "book_id": book.id,
    }

    response = await client.post("/borrows/", json=data)
    assert response.status_code == status.HTTP_201_CREATED


async def test_update_borrow(
    client: AsyncClient,
    factory: data_factory.FactoryCallback,
    async_session: AsyncSession,
):

    author = await factory(data_factory.AuthorFactory)
    assert not isinstance(author, Sequence)
    await async_session.refresh(author)

    book = await factory(data_factory.BookFactory, author_id=author.id)
    assert not isinstance(book, Sequence)
    await async_session.refresh(book)

    borrow = await factory(data_factory.BorrowFactory, book_id=book.id)
    assert not isinstance(borrow, Sequence)
    await async_session.refresh(borrow)

    response = await client.patch(f"/borrows/{borrow.id}/return/")

    assert response.status_code == status.HTTP_200_OK
