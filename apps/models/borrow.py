from datetime import date

from models.base import Base, int_pk
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Borrow(Base):
    __tablename__ = "borrow"
    id: Mapped[int_pk]
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"))
    reader_name: Mapped[str]
    borrow_date: Mapped[date] = mapped_column(
        server_default=func.now()  # pylint:disable=E1102
    )
    return_date: Mapped[date] = mapped_column(nullable=True)
    book: Mapped["Book"] = relationship(  # type:ignore[name-defined]
        lazy="joined", back_populates="borrow"
    )
