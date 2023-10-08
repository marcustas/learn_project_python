from abc import ABC, abstractmethod
from pydantic import BaseModel


class Publication(BaseModel):
    title: str
    author: str
    year: int



class BookModel(Publication):
    def display_info(self):
        return f'{self.title} - {self.author} from {self.year} year'

class MagazineModel(BookModel):
    month: str




class AbstractPublication(ABC):
    @abstractmethod
    def display_info(self):
        raise NotImplementedError


class Book(AbstractPublication):
    def __init__(self, model: Publication):
        self._model = model

    def __str__(self):
        return f'{self._model.title} - {self._model.author} from {self._model.year} year'

    def display_info(self):
        return str(self)

class Magazine(Book):
    pass

def log_book(func):
    def wrapped(self, book):
        result = func(self, book)
        if getattr(book, 'month', None):
            print(f'Magazine "{book.title}" was added')
        else:
            print(f'Book "{book.title}" was added')
        return result
    return wrapped


def check_book(func):
    def wrapped(self, book):
        result = func(self, book)
        if book not in self.books:
            print(f'The book "{book.title}" was removed')
        else:
            print(f'The book "{book.title}" doesn`t exist in the library')
            result = None
        return result
    return wrapped


class Library(Book):
    def __init__(self, model: Publication, books=None):
        super().__init__(model)
        if books is None:
            books = []
        self.books = books

    def all_books(self, iterable=None):
        print("List of books in the library:")
        for book in self.books:
            if getattr(book, 'month', None):
                print(f'Title: "{book.title}" / Author - {book.author} / Year: {book.year} / Month: {book.month}')
            else:
                print(f'Title: "{book.title}" / Author - {book.author} / Year: {book.year}')

    def return_book(self, author: str):
        author_name = [book for book in self.books if book.author == author]
        print(f"Books by {author}:")
        for book in author_name:
            print(book.display_info())

    @log_book
    def add_book(self, model: Publication):
        self.books.append(model)

    @check_book
    def remove_book(self, model: Publication):
        self.books.remove(model)

    def save_to_file(self, filename: str):  # Збереження списку книг в файл
        with open(filename, 'w') as file:
            for book in self.books:
                if getattr(book, 'month', None):
                    file.write(f'{book.title} - {book.author} - {book.year} - {book.month} \n')
                else:
                    file.write(f'{book.title} - {book.author} - {book.year} \n')

    def download_from_file(self, filename: str): # Завантаження списку книг з файлу
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                book_info = line.strip().split('-')
                if len(book_info)==4:
                    title, author, year, month = book_info
                    self.add_book(MagazineModel(title=title, author=author, year=int(year), month=month))
                elif len(book_info)==3:
                    title, author, year = book_info
                    self.add_book(BookModel(title=title, author=author, year=int(year)))


# Створення книг та журналів
book_1 = BookModel(title='Origin', author='Den Brown', year=2019)
book_2 = BookModel(title='IT', author='Steven King', year=1968)
book_3 = BookModel(title='1984', author='Georg Orwell', year=1949)
magazine_1 = MagazineModel(title='Forbs', author='Steve Forbs', year=2023, month='Jule')

# Створення бібліотеки
library = Library(model=book_1)

# Додавання книг та жірналів до списку в бібліотеці
library.add_book(book_1)
library.add_book(book_2)
library.add_book(book_3)
library.add_book(magazine_1)

# Вивід інформації по книгам та журналам
book_1.display_info()
book_2.display_info()
book_3.display_info()
magazine_1.display_info()

# Виведення списку книг та журналів
library.all_books()

# Повернення книги за ім'ям автора
library.return_book('Den Brown')

# Оновлений список книг та журналів
library.all_books()

# Збереження списку книг та журналів до файлу
library.save_to_file('List of books')

# Видалення книги з бібліотеки
library.remove_book(book_2)

# Завантаження списку книг та журналів з файлу
library.download_from_file('List of books')

# Виведення списку книг та журналів
library.all_books()
