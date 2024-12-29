from typing import Any, Awaitable, Callable, ParamSpec, Sequence, Type, TypeVar

import models
import sqlalchemy as sa
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession


fake = Faker()


class DataFactory:
    def __init__(self, session: AsyncSession) -> None:
        self.list_data: list[dict[str, Any]] = []
        self.model: models.TypeModel
        self.session = session
        self.response: Any

    # pylint: disable=W0613
    async def generate_data(self, count: int = 1, **kwargs): ...

    # pylint: disable=C0301
    async def write_to_db(self):
        if len(self.list_data) > 1:
            self.response = await self.session.scalars(
                sa.insert(self.model)
                .returning(self.model)
                .values(self.list_data)
            )
        else:
            self.response = await self.session.scalar(
                sa.insert(self.model)
                .returning(self.model)
                .values(self.list_data)
            )

    async def commit(self) -> models.MODEL | Sequence[models.MODEL]:
        await self.session.commit()
        if len(self.list_data) == 1:
            await self.session.refresh(self.response)
            return self.response
        return self.response.unique().all()


class AuthorFactory(DataFactory):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        self.model = models.Author

    async def generate_data(self, count=1, **kwargs) -> None:
        self.list_data.extend(
            {
                "first_name": kwargs.get("first_name", fake.first_name()),
                "last_name": kwargs.get("last_name", fake.last_name()),
                "birth_date": kwargs.get("birth_date", fake.date_of_birth()),
            }
            for _ in range(count)
        )
        await self.write_to_db()


class BookFactory(DataFactory):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        self.model = models.Book

    async def generate_data(self, count=1, **kwargs) -> None:
        self.list_data.extend(
            {
                "title": kwargs.get("title", fake.word()),
                "description": kwargs.get("description", fake.text()),
                "author_id": kwargs.get("author_id"),
                "count_copies": kwargs.get(
                    "count_copies", fake.pyint(min_value=0)
                ),
            }
            for _ in range(count)
        )
        await self.write_to_db()


class BorrowFactory(DataFactory):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        self.model = models.Borrow

    async def generate_data(self, count=1, **kwargs) -> None:
        self.list_data.extend(
            {
                "book_id": kwargs.get("book_id"),
                "reader_name": kwargs.get("reader_name", fake.name()),
                "return_date": kwargs.get("return_date", fake.date_object()),
            }
            for _ in range(count)
        )
        await self.write_to_db()


P = ParamSpec("P")
FACTORY = TypeVar("FACTORY", bound=DataFactory)


TypeFactory = Type[FACTORY]
FactoryCallback = Callable[P, Awaitable[models.MODEL | Sequence[models.MODEL]]]
