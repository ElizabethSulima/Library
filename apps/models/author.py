from datetime import date

from models.base import Base, int_pk
from sqlalchemy.orm import Mapped, relationship


class Author(Base):
    __tablename__ = "author"
    id: Mapped[int_pk]
    first_name: Mapped[str]
    last_name: Mapped[str]
    birth_date: Mapped[date]
    book: Mapped[list["Book"]] = relationship(  # type:ignore[name-defined]
        lazy="selectin", back_populates="author"
    )
