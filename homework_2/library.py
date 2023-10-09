import json
from typing import List
from abc import ABC, abstractmethod

from models import BookModel, MagazineModel
from decorators import log_adding_publication, is_publication_exist


class AbstractLibrary(ABC):
    @abstractmethod
    def add_publication(self, publication: BookModel):
        raise NotImplementedError

    @abstractmethod
    def remove_publication(self, publication: BookModel):
        raise NotImplementedError

    @abstractmethod
    def get_publication_by_author(self, author: str):
        raise NotImplementedError


class Library:
    def __init__(self):
        self.collection: List[BookModel] = []

    def get_publication_list(self) -> list[BookModel]:
        for publication in self.collection:
            print(publication)

    @log_adding_publication
    def add_publication(self, publication: BookModel):
        self.collection.append(publication)

    @is_publication_exist
    def remove_publication(self, publication: BookModel):
        if publication in self.collection:
            self.collection.remove(publication)

    def get_publication_by_author(self, author: str):
        for publication in self.collection:
            if publication.author == author:
                print(publication)

    def write_to_file(self):
        with open('publication_list.txt', 'w') as file:
            data = [publication.model_dump() for publication in self.collection]
            json.dump(data, file)

    def add_publications_from_file(self):
        with open('publication_list.txt', 'r') as file:
            data = json.load(file)
            self.collection = []
            for item in data:
                if 'month' in item:
                    publication = MagazineModel(**item)
                else:
                    publication = BookModel(**item)
                self.collection.append(publication)
        return self.collection
