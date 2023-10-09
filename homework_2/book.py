from abc import ABC, abstractmethod

from models import BookModel


class AbstractDocument(ABC):
    @abstractmethod
    def get_info(self):
        raise NotImplementedError


class Book(AbstractDocument):
    def __init__(self, model: BookModel):
        self.model = model

    def get_info(self) -> str:
        return f'Book title: {self.model.title} - Author: {self.model.author} - Year: {self.model.year}'

    def to_dict(self):
        return self.model.model_dump()
