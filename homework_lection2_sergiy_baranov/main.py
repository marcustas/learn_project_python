# Імпорт бібліотек.
import json
from pydantic import BaseModel
from abc import ABC
from typing import List, Type

# Декоратор для функції add_book.
# При кожному зверненні надрукує, що книга додана, назва книги та автор книги.
def log_add_book(func):
    def wrapper(self: "Library", book: Type[BaseModel]):
        print(f"Adding book: {book.title} by {book.author}")
        return func(self, book)
    return wrapper

# Декоратор функції "remove_book". Перевірити чи книга існує.
# Якщо так - повернеться в основну функцію, інакше надрукує, що книга не знайдена в бібліотеці.
def check_book_existence(func):
    def wrapper(self: "Library", book: Type[BaseModel]):
        if book in self.books:
            return func(self, book)
        else:
            print(f"Book not found in the library: {book.title} by {book.author}")
    return wrapper


# Cтворення класу "BookModel".
# При створенні об'єкта він буде переведений у рядок
# і буде виведено інформацію про книгу на підставі змінних "title", "author" та "year_published"
# Метод to_dict призначений для перетворення об'єкта класу BookModel у словник.
# Cтворює словник, де ключами є рядки "title", "author", "year_published".
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
# Абстрактний клас. На його основі буде створено клас "Library" з методами "add_book", "remove_book", "books_by_author".
class AbsLib(ABC):
    def add_book(self, book: Type[BaseModel]):
        pass
    def remove_book(self, book: Type[BaseModel]):
        pass
    def books_by_author(self, book: Type[BaseModel]):
        pass


# Клас "Library" успадковується від абстрактного класу "AbsLib".
class Library(AbsLib):
    def __init__(self):
        self.books: List[Type[BaseModel]] = []

    @log_add_book  # Декоратор для логування при додаванні книги
    # Метод додавання книги. Спочатку функція зайде до декоратора "log_add_book", а потім додасть книгу.
    def add_book(self, book: Type[BaseModel]):
        self.books.append(book)

    @check_book_existence  # Декоратор для перевірки наявності книги перед видаленням
    # Метод видалення книги.
    # Спочатку функція зайде в декоратор "check_book_existence",
    # який перевірить чи книга існує, а потім повернеться назад і видалить книгу,
    # якщо в декораторі умова if поверне true.
    def remove_book(self, book: Type[BaseModel]):
        if book in self.books:
            self.books.remove(book)
    # Ініціалізація змінної "index", для позначення того, що об'єкт цього класу повинен поводитися як ітератор.
    def __iter__(self):
        self.index = 0
        return self
    # Метод "__next__" дозволяє класу бути ітератором.
    # Цей метод перевіряє, чи поточний індекс "self.index" менший за загальну кількість елементів у списку "self.books".
    # Якщо так, це означає, що ще є елементи для ітерації, і збільшує "self.index" на 1 і повертає отриманий елемент.
    # Якщо умова "if" не виконується, ітерація закінчена.
    def __next__(self):
        if self.index < len(self.books):
            book = self.books[self.index]
            self.index += 1
            return book
        else:
            raise StopIteration
    # Цей метод призначений для отримання списку книг, які належать певному авторові.
    # Використовуємо "list comprehension" для створення нового списку,
    # який містить всі книги зі списку self.books, де поле author кожної книги співпадає з переданим параметром author.
    def books_by_author(self, author: str):
        return [book for book in self.books if book.author == author]

# Контекстний менеджер для збереження та завантаження даних бібліотеки з файлу
class LibraryFileManager:
    def __init__(self, file_name: str):
        self.file_name = file_name
    # Метод для запису даних у файл.
    # Контекстний менеджер відкриває файл із змінної "self.file_name" для запису "w", створює список data,
    # який містить словники , що представляють кожну книгу
    def save_library(self, library: Library):
        with open(self.file_name, 'w') as file:
            data = [book.to_dict() for book in library.books]
            json.dump(data, file, indent=4)
    # Метод для читання даних із файлу в змінній "self.file_name".
    # За допомогою виключення "try" та контекстного менеджера намагаємося відкрити файл на читання.
    # Завантажуємо дані з "json" файлу, циклом перебираємо кожен запис в "data", де кожен запис це одна книга.
    # Після завантаження всіх книг із файлу, повертається об'єкт "library", який містить усі книги.
    def load_library(self):
        try:
            with open(self.file_name, 'r') as file:
                data = json.load(file)
                library = Library()
                for book_data in data:
                    book = BookModel(**book_data)
                    library.add_book(book)
                return library
        except FileNotFoundError:
            return Library()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

if __name__ == "__main__":
    # Створюємо об'єкт класу "Library".
    library = Library()

    # Створюємо об'єкт "book1" ... класу "BookModel" із вхідними параметрами.
    book1 = BookModel(title="Book 1", author="Author 1", year_published=2000)
    book2 = BookModel(title="Book 2", author="Author 2", year_published=2005)
    journal1 = BookModel(title="Journal 1", author="Author 1", year_published=2020)

    # Викликає метод "add_book" з об'єкта "library" для додавання книги.
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

    # Використовуємо контекстний менеджер для збереження бібліотеки в файл
    with LibraryFileManager("library.json") as file_manager:
        file_manager.save_library(library)
        print("\nBooks saved to library.json")

    library.remove_book(book2)

    print("\nList of books in the library after removing Book 2:")
    for book in library:
        print(book)

    # Використовуємо контекстний менеджер для завантаження бібліотеки з файлу
    with LibraryFileManager("library.json") as file_manager:
        loaded_library = file_manager.load_library()
        print("\nBooks loaded from library.json")

    print("\nList of books in the library after loading from file:")
    for book in loaded_library:
        print(book)
