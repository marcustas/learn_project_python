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
    last_printed_day: date


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


@contextmanager
def create_list(filename, mode):
    file = open(filename, mode)
    yield file
    file.close()


@contextmanager
def load_list_books(filename):
    with open(filename, 'r') as file:
        book_list = file.readlines()
        yield book_list


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
        self.list_of_books.remove(reading)

    def books_on_the_library(self):
        for book in self.list_of_books:
            print(book.reading_info())

    def books_generator(self, author):
        for book in self.list_of_books:
            if book._model.author == author:
                yield f'Book {book._model.title} writed by {book._model.author}'

    def download_list_manager(self):
        data = []
        for book in self.list_of_books:
            data.append({
                'title': book._model.title,
                'author': book._model.author,
                'created_date': book._model.created_date.isoformat(),
            })

        with open('book_list1.json', 'w') as file:
            json.dump(data, file, indent=4)

    def read_list(self, file):
        with open(file, 'r') as file_r:
            book_data = json.load(file_r)
            for book_info in book_data:
                title = book_info['title']
                author = book_info['author']
                created_date = date.fromisoformat(book_info['created_date'])
                book_model = BookModel(title=title, author=author, created_date=created_date)
                book = Book(book_model)
                self.list_of_books.append(book)

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
    last_printed_day=date(1917, 1, 15),
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

library.download_list_manager()

library.del_material('Forbes')
library.books_on_the_library()

library.read_list('book_list1.json')
library.books_on_the_library()



