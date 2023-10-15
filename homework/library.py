import json
from contextlib import contextmanager
from models import BookModel, MagazineModel
from publications import AbstractPublication, Book, Magazine


def log_action(func):
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        print(f'Function {func.__name__} was executed for publication: {result}')
        return result

    return wrapper


def is_book_exist(func):
    def wrapper(self, publication: AbstractPublication):
        if publication in self.publications:
            print(f'Publication {publication} is in the Library and will be deleted')
            func(self, publication)
        else:
            print(f"There is no such publication as {publication} in the Library. It can not be deleted")
        return func

    return wrapper


@contextmanager
def file_opener(filename, mode):
    file = open(filename, mode)
    yield file
    file.close()


class Library:
    publications: list[AbstractPublication]

    def __init__(self):
        self.publications = []

    def iterate_books(self):
        print("Iterating books in the Library:")
        library_iterator = iter(self.publications)
        for publication in library_iterator:
            print(publication)

    @log_action
    def add_book_to_library(self, publication: AbstractPublication):
        self.publications.append(publication)
        return publication.__str__()

    @is_book_exist
    def delete_book_from_library(self, publication: AbstractPublication):
        self.publications.remove(publication)

    @log_action
    def get_books_from_library(self):
        return [publications.display_info() for publications in self.publications]

    def get_books_from_library_by_author(self, author_name):
        print(f"There are publication found by autor name = {author_name}:")
        for publication in self.publications:
            if publication._model.author == author_name:
                yield publication.__str__()

    def read_library_from_file(self, filename: str):
        print("Reading library from the file")
        with file_opener(filename, 'r') as file:
            data = json.load(file)
            self.publications = []
            for item in data:
                if 'month' in item:
                    publication = Magazine(MagazineModel(**item))
                else:
                    publication = Book(BookModel(**item))
                self.publications.append(publication)
        return self.publications

    def write_library_to_file(self, filename: str):
        print("Writing library to the file...")
        with file_opener(filename, 'w') as file:
            json.dump([publication.to_dict() for publication in self.publications], file)
