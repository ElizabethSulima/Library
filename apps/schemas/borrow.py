from datetime import date

from pydantic import BaseModel, ConfigDict
from schemas.book import BookResponse


class Borrow(BaseModel):
    reader_name: str


class BorrowCreate(Borrow):
    book_id: int


class BorrowResponse(Borrow):
    id: int
    book: BookResponse
    borrow_date: date
    return_date: date | None = None
    model_config = ConfigDict(from_attributes=True)
