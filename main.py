from pydantic import BaseModel
import json

# Клас "Книга" з моделлю Pydantic
class BookModel(BaseModel):
    title: str
    author: str
    publication_year: int

    def __str__(self):
        return f"Назва: {self.title}, Автор: {self.author}, Рік видання: {self.publication_year}"

# Клас "Бібліотека"
class Library:
    def __init__(self):
        self.books = []

    # Декоратор для логування додавання книги
    @staticmethod
    def log_add_book(func):
        def wrapper(self, book):
            result = func(self, book)
            print(f"Додано книгу: {book}")
            return result
        return wrapper

    # Декоратор для перевірки наявності книги перед видаленням
    @staticmethod
    def check_book_existence(func):
        def wrapper(self, book_title):
            if any(book.title == book_title for book in self.books):
                result = func(self, book_title)
                print(f"Книгу '{book_title}' видалено з бібліотеки.")
                return result
            else:
                print(f"Книги '{book_title}' немає у бібліотеці.")
        return wrapper

    # Додавання книги до бібліотеки
    @log_add_book
    def add_book(self, book):
        self.books.append(book)

    # Видалення книги з бібліотеки
    @check_book_existence
    def remove_book(self, book_title):
        self.books = [b for b in self.books if b.title != book_title]

    # Виведення списку книг
    def list_books(self):
        return self.books

    # Генератор, який повертає книги за іменем автора
    def books_by_author(self, author_name):
        for book in self.books:
            if book.author == author_name:
                yield book

    # Збереження списку книг у файл
    def save_books_to_file(self, file_name):
        with open(file_name, 'w') as file:
            json.dump([book.dict() for book in self.books], file)

    # Додавання книг з файлу до бібліотеки
    def add_books_from_file(self, file_name):
        with open(file_name, 'r') as file:
            book_data = json.load(file)
            for data in book_data:
                book = BookModel(**data)
                self.add_book(book)

if __name__ == "__main__":
    # Створення бібліотеки
    library = Library()

    # Створення інстансів книг та журналу
    book1 = BookModel(title="Книга 1", author="Автор 1", publication_year=2020)
    book2 = BookModel(title="Книга 2", author="Автор 2", publication_year=2019)
    journal1 = BookModel(title="Журнал 1", author="Автор 3", publication_year=2022)

    # Додавання книг та журналу до бібліотеки
    library.add_book(book1)
    library.add_book(book2)
    library.add_book(journal1)

    # Виведення списку книг у бібліотеці
    print("Список книг у бібліотеці:")
    for book in library.list_books():
        print(book)

    # Виведення списку книг бібліотеки по імені автора
    print("\nКниги автора 'Автор 1':")
    for book in library.books_by_author("Автор 1"):
        print(book)

    # Збереження списку книг у файл
    library.save_books_to_file("library_data.json")

    # Видалення книги з бібліотеки
    library.remove_book("Книга 1")

    # Виведення списку книг після видалення
    print("\nСписок книг у бібліотеці після видалення:")
    for book in library.list_books():
        print(book)

    # Додавання книг з файлу до бібліотеки
    library.add_books_from_file("library_data.json")

    # Виведення списку книг бібліотеки після додавання
    print("\nСписок книг у бібліотеці після додавання з файлу:")
    for book in library.list_books():
        print(book)


print(Library.list_books())