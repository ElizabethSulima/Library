from typing import Sequence

from crud import author as ca
from models import Author
from schemas import author as sa
from sqlalchemy.ext.asyncio import AsyncSession


class AuthorServices:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = ca.Author(self.session)

    async def get_authors(self) -> Sequence[Author]:
        return await self.repository.get_items()

    async def get_author_by_id(self, author_id: int) -> Author:
        return await self.repository.get_item_id(author_id)

    async def post_author(self, author_data: sa.Author) -> Author:
        author: Author = await self.repository.create_item(
            author_data.model_dump()
        )
        await self.session.commit()
        await self.session.refresh(author)
        return author

    async def put_author(
        self, author_id: int, author_data: sa.AuthorUpdate
    ) -> Author:
        data = author_data.model_dump(exclude_unset=True)
        data["id"] = author_id
        author: Author = await self.repository.put_item(data)
        await self.session.commit()
        await self.session.refresh(author)
        return author

    async def delete_author(self, author_id: int) -> None:
        await self.repository.delete_item(author_id)
        await self.session.commit()
