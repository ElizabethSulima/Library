from datetime import date

from pydantic import BaseModel, ConfigDict


class Author(BaseModel):
    first_name: str
    last_name: str
    birth_date: date


class AuthorCreate(Author):
    pass


class AuthorResponse(Author):
    id: int
    model_config = ConfigDict(from_attributes=True)


class AuthorUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
