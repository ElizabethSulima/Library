from typing import Type, TypeVar

from models.author import Author
from models.base import Base
from models.book import Book
from models.borrow import Borrow


MODEL = TypeVar("MODEL", bound=Base)
TypeModel = Type[MODEL]
