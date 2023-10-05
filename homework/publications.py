from abc import ABC, abstractmethod
from models import BookModel, MagazineModel


class AbstractPublication(ABC):
    @abstractmethod
    def display_info(self):
        raise NotImplementedError


class Book(AbstractPublication):
    def __init__(self, model: BookModel):
        self._model = model

    def __str__(self):
        return f'Publication: {self._model.name} - {self._model.author}, year - {self._model.year_of_publish}'

    def display_info(self):
        return self.__str__()

    def to_dict(self):
        return self._model.dict()


class Magazine(AbstractPublication):

    def __init__(self, model: MagazineModel):
        self._model = model

    def __str__(self):
        return f'Publication: {self._model.name} - {self._model.author}, year - {self._model.year_of_publish}, month - {self._model.month}'

    def display_info(self):
        return self.__str__()

    def to_dict(self):
        return self._model.dict()