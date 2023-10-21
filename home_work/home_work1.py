import json
from pydantic import BaseModel
from abc import (
    ABC,
    abstractmethod
)
from datetime import date
from contextlib import contextmanager


class BookModel(BaseModel):
    title: str
    author: str
    created_date: date


class JournalModel(BookModel):
    theme: str


class AbstractReading(ABC):
    @abstractmethod
    def reading_info(self):
        raise NotImplementedError


class Book(AbstractReading):
    def __init__(self, model: BookModel):
        self._model = model

    def reading_info(self):
        return f'Book {self._model.title} writed by {self._model.author} from {self._model.created_date}year'


class Journal(Book):
    def __init__(self, model: JournalModel):
        self._model = model


def add_book_notif(func):
    def wrapper(self, reading):
        result = func(self, reading)
        return f'Book{reading._model.title}was added'
    return wrapper


def check_book(func):
    def wrapper(self, title):
        for reading in self.list_of_books:
            if reading._model.title == title:
                result = func(self, reading)
                return f'Book {reading._model.title} deleted'
    return wrapper


class Library:
    def __init__(self):
        self.list_of_books: list = []

    @add_book_notif
    def add_material(self, reading):
        self.list_of_books.append(reading)

    @check_book
    def del_material(self, reading):
        try:
            self.list_of_books.remove(reading)
        except:
            raise ValueError(f'Book{reading._model.title} is not found')

    def books_on_the_library(self):
        for book in self.list_of_books:
            print(book.reading_info())

    def books_generator(self, author):
        for book in self.list_of_books:
            if book._model.author == author:
                yield f'Book {book._model.title} writed by {book._model.author}'

    @contextmanager
    def download_list_manager(self, filename):
        data = []
        for book in self.list_of_books:
            dictionary = dict(book._model)
            if dictionary['created_date']:
                dictionary['created_date'] = dictionary['created_date'].isoformat()
            data.append(dictionary)
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        yield

    @contextmanager
    def read_list(self, filename):
        with open(filename, 'r') as file_r:
            book_data = json.load(file_r)
            books = [Book(BookModel(**data)) for data in book_data]
            self.list_of_books.extend(books)
        yield


book_model1 = BookModel(
    title='Sherlock Holmes',
    author='Arthur Conan Doyle',
    created_date=date(1887, 1, 1),
)
book_model2 = BookModel(
    title='Code Complete',
    author='Steve McConnell',
    created_date=date(2010, 1, 1),
)
book_model3 = BookModel(
    title='Harry Potter',
    author='Joanne Rowling',
    created_date=date(1997, 1, 1),
)
journal_model1 = JournalModel(
    title='Forbes',
    author='Charles Forbes',
    created_date=date(1917, 1, 1),
    theme='Politic',
)

book1 = Book(book_model1)
book2 = Book(book_model2)
book3 = Book(book_model3)
journal1 = Journal(journal_model1)

library = Library()
library.add_material(book1)
library.add_material(book2)
library.add_material(book3)
library.add_material(journal1)

library.books_on_the_library()

for book_info in library.books_generator('Arthur Conan Doyle'):
    print(book_info)

with library.download_list_manager('book_list.json'):
    pass

library.del_material('Forbes')
library.books_on_the_library()

with library.read_list('book_list.json'):
    pass
library.books_on_the_library()
