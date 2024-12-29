import models
import sqlalchemy as sa
from crud.common import Base


class Borrow(Base):
    def __init__(self, session):
        super().__init__(session)
        self.model = models.Borrow

    async def get_borrow(self, borrow_id: int) -> models.Borrow | None:
        return await self.session.scalar(
            sa.select(self.model).where(self.model.id == borrow_id)
        )
