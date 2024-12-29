from pydantic import BaseModel, ConfigDict


class Book(BaseModel):
    title: str
    description: str
    author_id: int
    count_copies: int


class BookCreate(Book):
    pass


class BookResponse(Book):
    id: int
    model_config = ConfigDict(from_attributes=True)


class BookUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    author_id: int | None = None
    count_copies: int | None = None
