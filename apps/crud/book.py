import models
import sqlalchemy as sa
from crud.common import Base


class Book(Base):
    def __init__(self, session):
        super().__init__(session)
        self.model = models.Book

    async def get_book(self, book_id: int) -> models.Book | None:
        return await self.session.scalar(
            sa.select(self.model).where(self.model.id == book_id)
        )
