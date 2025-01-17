from typing import Annotated, Type, TypeVar

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, mapped_column


int_pk = Annotated[int, mapped_column(primary_key=True)]


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_`%(constraint_name)s`",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%"
            "(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


MODEL = TypeVar("MODEL", bound=Base)

TypeModel = Type[MODEL]
