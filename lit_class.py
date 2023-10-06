from pydantic import BaseModel
from abc import ABC, abstractmethod

class AbstractLiterature(ABC):
    """Abstract Class, which forces subclasses to have certain methods"""
    @abstractmethod
    def show_description(self):
        raise NotImplementedError("Each piece of literature must have the show_description method")

class BookModel(BaseModel):
    title: str
    author: str
    year: int
    lib_id: int


class MagazineModel(BookModel):
    month: str
    type: str


class Book(AbstractLiterature):

    def __init__(self, model: BookModel):
        self._model = model

    def __str__(self):
        return f"The book \"{self._model.title}\" was written in {self._model.year} by {self._model.author}"

    def show_description(self):
        return str(self)


class Magazine(Book):
    def __init__(self, model: MagazineModel):
        self.model = model

    def __str__(self):
        return f"The {self.model.type} magazine \"{self.model.title}\" " \
               f"was published in {self.model.month} of {self.model.year} by {self.model.author}"

    def show_description(self):
        return str(self)
