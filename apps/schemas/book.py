from pydantic import BaseModel, ConfigDict
from schemas.author import AuthorResponse


class Book(BaseModel):
    title: str
    description: str
    count_copies: int


class BookCreate(Book):
    author_id: int


class BookResponse(Book):
    id: int
    author: AuthorResponse
    model_config = ConfigDict(from_attributes=True)


class BookUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    author_id: int | None = None
    count_copies: int | None = None
