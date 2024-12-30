from models.base import Base, int_pk
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Book(Base):
    __tablename__ = "book"
    id: Mapped[int_pk]
    title: Mapped[str]
    description: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
    count_copies: Mapped[int]
    author: Mapped["Author"] = relationship(  # type:ignore[name-defined]
        lazy="joined", back_populates="book"
    )
    borrow: Mapped[list["Borrow"]] = relationship(  # type:ignore[name-defined]
        lazy="selectin", back_populates="book"
    )
