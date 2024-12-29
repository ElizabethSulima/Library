from datetime import date
from typing import Sequence

import fastapi as fa
from crud import book as cbook
from crud import borrow as cb
from models import Borrow
from schemas import borrow as sb
from sqlalchemy.ext.asyncio import AsyncSession


class BorrowServices:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = cb.Borrow(self.session)
        self.repository_book = cbook.Book(self.session)

    async def get_borrows(self) -> Sequence[Borrow]:
        return await self.repository.get_items()

    async def get_borrow_by_id(self, borrow_id: int) -> Borrow:
        return await self.repository.get_item_id(borrow_id)

    async def post_borrow(self, borrow_data: sb.Borrow) -> Borrow:
        data = borrow_data.model_dump()
        book = await self.repository_book.get_book(borrow_data.book_id)
        if book is None:
            raise fa.HTTPException(
                status_code=fa.status.HTTP_404_NOT_FOUND,
                detail="Book not found",
            )
        if book.count_copies <= 0:
            raise fa.HTTPException(
                status_code=fa.status.HTTP_400_BAD_REQUEST,
                detail="There are no available copies to issue",
            )
        book.count_copies -= 1

        borrow: Borrow = await self.repository.create_item(data)
        await self.session.commit()
        await self.session.refresh(borrow)
        return borrow

    async def patch_borrow(self, borrow_id: int) -> Borrow:
        borrow = await self.repository.get_borrow(borrow_id)

        if borrow is None:
            raise fa.HTTPException(
                status_code=fa.status.HTTP_404_NOT_FOUND,
                detail="Borrow not found",
            )
        book = await self.repository_book.get_book(borrow.book_id)
        if book:
            book.count_copies += 1

        data = {"id": borrow_id, "return_date": date.today()}

        response: Borrow = await self.repository.put_item(data)
        await self.session.commit()
        await self.session.refresh(response)
        return response
