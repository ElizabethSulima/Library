from datetime import date

from pydantic import BaseModel, ConfigDict


class Borrow(BaseModel):
    reader_name: str
    book_id: int


class BorrowCreate(Borrow):
    pass


class BorrowResponse(Borrow):
    id: int
    borrow_date: date
    return_date: date | None = None
    model_config = ConfigDict(from_attributes=True)
