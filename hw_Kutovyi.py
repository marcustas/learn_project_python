from typing import List
from pydantic import BaseModel


class BookModel(BaseModel):
    title: str
    author: str
    year: int

    def __str__(self):
        return f"{self.title} ({self.author}, {self.year})"



class Library:
    def __init__(self):
        self.books: List[BookModel] = []

    def add_book(self, book: BookModel):
        self.books.append(book)

    def remove_book(self, title: str):
        self.books = [book for book in self.books if book.title != title]

    def list_books(self):
        for book in self.books:
            print(book)

    def author_books(self, author: str):
        for book in self.books:
            if book.author == author:
                print(book)

    # Ітератор, що дозволяє проходитися по всіх книгах у бібліотеці
    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.books):
            book = self.books[self.index]
            self.index += 1
            return book
        raise StopIteration


# Декоратор для логування при додаванні нової книги до бібліотеки
def log_add_book(func):
    def wrapper(library, book):
        print(f"Додаємо книгу: {book}")
        func(library, book)
        print(f"Книга {book.title} додана до бібліотеки")

    return wrapper


# Декоратор, який перевіряє наявність книги в бібліотеці перед її видаленням
def check_book_existence(func):
    def wrapper(library, title):
        for book in library.books:
            if book.title == title:
                func(library, title)
                print(f"Книга {title} видалена з бібліотеки")
                return
        print(f"Книга {title} не знайдена в бібліотеці")

    return wrapper


# Контекстний менеджер
class LibraryFileManager:
    def __init__(self, library, filename):
        self.library = library
        self.filename = filename

    def __enter__(self):
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    data = line.strip().split(',')
                    title, author, year = data
                    book = BookModel(title=title, author=author, year=int(year))
                    self.library.add_book(book)
            print(f"Завантажено книги з файлу {self.filename}")
        except FileNotFoundError:
            print(f"Файл {self.filename} не знайдено. Створено новий файл.")

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        with open(self.filename, 'w') as file:
            for book in self.library.books:
                file.write(f"{book.title},{book.author},{book.year}\n")
        print(f"Список книг збережено у файл {self.filename}")


if __name__ == "__main__":
    library = Library()

    # Створення інстансу книги та журналу
    book1 = BookModel(title="Clean Code", author="Robert C", year=2015)
    book2 = BookModel(title="Вивчаємо Python", author="Марк Лутц", year=2022)

    # Додавання їх у бібліотеку
    library.add_book(book1)
    library.add_book(book2)

    # Виведення списку книг у бібліотеці
    print("Список книг у бібліотеці:")
    library.list_books()

    # Виведення списку книг бібліотеки по імені автора
    print("\nСписок книг автора Author1:")
    library.author_books("Author1")

    # Збереження списку книг у файл
    with LibraryFileManager(library, "library.txt"):
        pass

    # Видалення книги з бібліотеки
    @check_book_existence
    def remove_book(library, title):
        library.remove_book(title)

    remove_book(library, "Book1")

    # Виведення списку книг після видалення
    print("\nСписок книг у бібліотеці після видалення:")
    library.list_books()

    # Додавання книг з файлу в бібліотеку
    with LibraryFileManager(library, "library.txt"):
        pass

    # Виведення списку книг бібліотеки після додавання
    print("\nСписок книг у бібліотеці після додавання з файлу:")
    library.list_books()
