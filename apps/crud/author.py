import models
from crud.common import Base


class Author(Base):
    def __init__(self, session):
        super().__init__(session)
        self.model = models.Author
