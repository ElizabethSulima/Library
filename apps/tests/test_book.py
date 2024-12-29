from typing import Sequence

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from tests import factory as data_factory


pytestmark = pytest.mark.anyio


async def test_get_books(
    client: AsyncClient,
    factory: data_factory.FactoryCallback,
    async_session: AsyncSession,
):
    author = await factory(data_factory.AuthorFactory)
    assert not isinstance(author, Sequence)
    await async_session.refresh(author)

    await factory(data_factory.BookFactory, 10, author_id=author.id)
    response = await client.get("/books/")
    assert response.status_code == status.HTTP_200_OK


async def test_get_book_id(
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

    response = await client.get(f"/books/{book.id}/")
    assert response.status_code == status.HTTP_200_OK


async def test_create_book(
    client: AsyncClient,
    factory: data_factory.FactoryCallback,
    async_session: AsyncSession,
):
    author = await factory(data_factory.AuthorFactory)
    assert not isinstance(author, Sequence)
    await async_session.refresh(author)

    data = {
        "title": "Utopia",
        "description": "Short story",
        "author_id": author.id,
        "count_copies": 25,
    }

    response = await client.post("/books/", json=data)
    assert response.status_code == status.HTTP_201_CREATED


async def test_update_book(
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

    updated_data = {
        "title": "Utopia",
        "description": "Short story",
    }
    response = await client.put(f"/books/{book.id}/", json=updated_data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "Utopia"
    assert response.json()["description"] == "Short story"


async def test_delete_book(
    client: AsyncClient, factory: data_factory.FactoryCallback
):
    author = await factory(data_factory.AuthorFactory)
    assert not isinstance(author, Sequence)

    response = await client.delete(f"/books/{author.id}/")
    assert response.status_code == status.HTTP_200_OK
