from typing import Sequence

from crud import book as cb
from models import Book
from schemas import book as sb
from sqlalchemy.ext.asyncio import AsyncSession


class BookServices:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = cb.Book(self.session)

    async def get_books(self) -> Sequence[Book]:
        return await self.repository.get_items()

    async def get_book_by_id(self, book_id: int) -> Book:
        return await self.repository.get_item_id(book_id)

    async def post_book(self, book_data: sb.Book) -> Book:
        book: Book = await self.repository.create_item(book_data.model_dump())
        await self.session.commit()
        await self.session.refresh(book)
        return book

    async def put_book(self, book_id: int, book_data: sb.BookUpdate) -> Book:
        data = book_data.model_dump(exclude_unset=True)
        data["id"] = book_id
        book: Book = await self.repository.put_item(data)
        await self.session.commit()
        await self.session.refresh(book)
        return book

    async def delete_book(self, book_id: int) -> None:
        await self.repository.delete_item(book_id)
        await self.session.commit()
