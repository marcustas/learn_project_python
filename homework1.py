from typing import List
from pydantic import BaseModel
from abc import ABC, abstractmethod

# Pydantic модель для книги
class BookModel(BaseModel):
    title: str
    author: str
    year: int

    def __str__(self):
        return f"{self.title} ({self.author}, {self.year})"

#Абстрактний клас
class AbstractLiterature(ABC):
    @abstractmethod
    def litinfo(self):
        raise NotImplementedError

# Клас "Книга" з методом для повернення інформації про книгу
class Book(AbstractLiterature):
    def __init__(self, book_model: BookModel):
        self.book_model = book_model

    def __str__(self):
        return str(self.book_model)

    #Імплементація абстрактного методу
    def litinfo(self):
        return self.__str__()

# Клас "Журнал", який наслідується від "Книги"
class Journal(Book):
    pass
# Клас "Бібліотека" з атрибутом у вигляді списку книг (зроблений приватним)
class Library:
    def __init__(self):
        self.__books: List[Book] = []

    # Функції для перегляду і взаємодії з приватним класом
    def get_books(self):
        return self.__books

    def set_books(self, books):
        self.__books = books


    # Декоратор, який пише лог при додаванні нової книги у бібліотеку
    def add_log(func):
        def wrapper(self, book):
            print(f"\nAdding the book: {book}")
            result = func(self, book)
            print("\nList of books in the library after addition:")
            for b in self.get_books():
                print(b)
            return result

        return wrapper

    # Декоратор, який перевіряє наявність книги у бібліотеці перед видаленням
    def check_existence(func):
        def wrapper(self, book):
            if book in self.get_books():
                print(f"\nRemoving the book '{book}'")
                result = func(self, book)
            else:
                print(f"Book '{book}' has not been found in the library")
                result = None
            return result

        return wrapper

    @add_log
    def add_book(self, book: Book):
        self.get_books().append(book)

    @check_existence
    def remove_book(self, book: Book):
        self.get_books().remove(book)

    # Ітератор, який дозволяє проходитися по всіх книгах у бібліотеці
    def __iter__(self):
        return iter(self.get_books())

    # Генератор, який повертає книги за ім'ям одного автора
    def books_by_author(self, author: str):
        for book in self.get_books():
            if book.book_model.author == author:
                yield book

    # Збереження списку книг до файлу за допомогою контекстного менеджеру
    def save_to_file(self, filename: str):
        with open(filename, 'w') as file:
            for book in self.get_books():
                file.write(f"{book.book_model.title},{book.book_model.author},{book.book_model.year}\n")

    # Завантаження списку книг з файлу за допомогою контекстного менеджеру
    def load_from_file(self, filename: str):
        with open(filename, 'r') as file:
            lines = file.readlines()
            print("\nImporting from file:")
            for line in lines:
                title, author, year = line.strip().split(',')
                book_model = BookModel(title=title, author=author, year=int(year))
                self.add_book(Book(book_model))

# Використання класів і об'єктів
if __name__ == "__main__":
    library = Library()

    book1 = Book(BookModel(title="Ulysses", author="James Joyce", year=1922))
    book2 = Book(BookModel(title="The Great Gatsby", author="F. Scott Fitzgerald", year=1925))
    journal = Journal(BookModel(title="The Economist", author="Tom Standage", year=2023))

    # You can access and modify _books using the get_books and set_books methods
    library.set_books([book1, book2, journal])

    print("\nList of books in the library:")
    for book in library.get_books():
        print(book)

    print("\nList of books by author 'James Joyce':")
    for book in library.books_by_author("James Joyce"):
        print(book)

    library.save_to_file("library.txt")

    library.remove_book(book2)

    print("\nList of books after removal:")
    for book in library:
        print(book)

    library.load_from_file("library.txt")