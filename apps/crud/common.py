from typing import Any, Sequence

import sqlalchemy as sa
from fastapi import HTTPException, status
from models.base import MODEL, TypeModel
from sqlalchemy.ext.asyncio import AsyncSession


class Base:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.model: TypeModel

    async def create_item(self, data: dict[str, Any]) -> MODEL:
        item = await self.session.scalar(
            sa.insert(self.model).returning(self.model).values(**data)
        )
        return item  # type: ignore[return-value]

    async def get_items(self) -> Sequence[MODEL]:
        result = await self.session.scalars(
            sa.select(self.model).order_by(self.model.id.desc())
        )
        return result.unique().all()

    async def get_item_id(self, item_id: int) -> MODEL:
        stmt = sa.select(self.model).where(self.model.id == item_id)
        result = await self.session.scalar(stmt)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model.__name__} not found",
            )
        return result

    async def put_item(self, data: dict[str, Any]) -> MODEL:
        item_id = data.pop("id")
        stmt = (
            sa.update(self.model)
            .returning(self.model)
            .where(self.model.id == item_id)
            .values(**data)
        )
        item = await self.session.scalar(stmt)
        await self.session.flush()
        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model.__name__} not found",
            )
        return item

    async def delete_item(self, item_id: int) -> None:
        await self.session.execute(
            sa.delete(self.model).where(self.model.id == item_id)
        )
