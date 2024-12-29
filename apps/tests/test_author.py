from typing import Sequence

import pytest
from fastapi import status
from httpx import AsyncClient
from tests import factory as data_factory


pytestmark = pytest.mark.anyio


async def test_get_authors(
    client: AsyncClient, factory: data_factory.FactoryCallback
):
    await factory(data_factory.AuthorFactory, 10)
    response = await client.get("/authors/")
    assert response.status_code == status.HTTP_200_OK


async def test_get_author_id(
    client: AsyncClient, factory: data_factory.FactoryCallback
):
    author = await factory(data_factory.AuthorFactory)
    assert not isinstance(author, Sequence)
    response = await client.get(f"/authors/{author.id}/")
    assert response.status_code == status.HTTP_200_OK


async def test_create_author(client: AsyncClient):
    data = {
        "first_name": "Bob",
        "last_name": "Shayh",
        "birth_date": "2024-02-04",
    }
    response = await client.post("/authors/", json=data)
    assert response.status_code == status.HTTP_201_CREATED


async def test_update_author(
    client: AsyncClient, factory: data_factory.FactoryCallback
):

    author = await factory(data_factory.AuthorFactory)
    assert not isinstance(author, Sequence)

    updated_data = {
        "first_name": "Jonh",
        "last_name": "Nolan",
    }
    response = await client.put(f"/authors/{author.id}/", json=updated_data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["first_name"] == "Jonh"
    assert response.json()["last_name"] == "Nolan"


async def test_delete_author(
    client: AsyncClient, factory: data_factory.FactoryCallback
):
    author = await factory(data_factory.AuthorFactory)
    assert not isinstance(author, Sequence)

    response = await client.delete(f"/authors/{author.id}/")
    assert response.status_code == status.HTTP_200_OK
