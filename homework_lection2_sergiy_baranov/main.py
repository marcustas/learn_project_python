import json
from pydantic import BaseModel
from abc import ABC

# Клас "Книга"
class BookModel(BaseModel):
    title: str
    author: str
    year_published: int

    def __str__(self):
        return f"Title: {self.title}, Author: {self.author}, Year Published: {self.year_published}"

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "year_published": self.year_published
        }


class AbsLib(ABC):
    def add_book(self, book):
        pass
    def remove_book(self, book):
        pass
    def books_by_author(self, book):
        pass

# Клас "Бібліотека"
class Library(AbsLib):
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, book):
        if book in self.books:
            self.books.remove(book)

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.books):
            book = self.books[self.index]
            self.index += 1
            return book
        else:
            raise StopIteration

    def books_by_author(self, author):
        return [book for book in self.books if book.author == author]

# Декоратори
def log_add_book(func):
    def wrapper(self, book):
        print(f"Adding book: {book.title} by {book.author}")
        return func(self, book)
    return wrapper

def check_book_existence(func):
    def wrapper(self, book):
        if book in self.books:
            return func(self, book)
        else:
            print(f"Book not found in the library: {book.title} by {book.author}")
    return wrapper

# Контекстний менеджер
class LibraryFileManager:
    def __init__(self, library, file_name):
        self.library = library
        self.file_name = file_name

    def __enter__(self):
        try:
            with open(self.file_name, 'r') as file:
                data = json.load(file)
                for book_data in data:
                    book = BookModel(**book_data)
                    self.library.add_book(book)
        except FileNotFoundError:
            pass
        return self.library

    def __exit__(self, exc_type, exc_value, traceback):
        with open(self.file_name, 'w') as file:
            data = [book.to_dict() for book in self.library.books]
            json.dump(data, file, indent=4)

if __name__ == "__main__":
    library = Library()

    book1 = BookModel(title="Book 1", author="Author 1", year_published=2000)
    book2 = BookModel(title="Book 2", author="Author 2", year_published=2005)
    journal1 = BookModel(title="Journal 1", author="Author 1", year_published=2020)

    library.add_book(book1)
    library.add_book(book2)
    library.add_book(journal1)

    print("List of books in the library:")
    for book in library:
        print(book)

    print("\nBooks by Author 1:")
    author_books = library.books_by_author("Author 1")
    for book in author_books:
        print(book)

    with LibraryFileManager(library, "library.json"):
        print("\nBooks saved to library.json")

    library.remove_book(book2)

    print("\nList of books in the library after removing Book 2:")
    for book in library:
        print(book)

    with LibraryFileManager(library, "library.json"):
        print("\nBooks loaded from library.json")

    print("\nList of books in the library after loading from file:")
    for book in library:
        print(book)
