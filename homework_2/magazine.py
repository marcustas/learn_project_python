from abc import ABC, abstractmethod

from models import MagazineModel


class AbstractDocument(ABC):
    @abstractmethod
    def get_info(self):
        raise NotImplementedError


class Magazine(AbstractDocument):
    def __init__(self, model: MagazineModel):
        self.model = model

    def get_info(self) -> str:
        return (f'Magazine title: {self.model.title} - Author: {self.model.author} - '
                f'Year: {self.model.year} -Month: {self.model.month}')

    def to_dict(self):
        return self.model.model_dump()
