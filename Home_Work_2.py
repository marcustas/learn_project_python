from pydantic import BaseModel
from pprint import pprint
from abc import ABC, abstractmethod
from functools import wraps


class BookModel(BaseModel):
    name: str
    author: str
    issue_date: str


class MagazineModel(BookModel):
    style: str


class AbstractClass(ABC):
    @abstractmethod
    def display_author_name(self):
        raise NotImplementedError


class Book(AbstractClass):
    # book_list = list()
    book_dict = dict()

    def __init__(self, book: BookModel):
        self.name = book.name
        self.author = book.author
        self.issue_date = book.issue_date
        # self.book_list.append(self.__repr__())
        self.book_dict.setdefault(self.author, []).append(self.name)

    def __str__(self):
        return (f'Book "{self.name.title()}" was written by {self.author.title()} '
                f'and issued {self.issue_date}.')

    def __repr__(self):
        return f'"{self.name.title()}"'

    def display_author_name(self):
        return f'Author`s name of {self.name} is {self.author}'


class Magazine(Book):
    def __init__(self, magazine: MagazineModel):
        super().__init__(magazine)
        self.style = magazine.style

    def __str__(self):
        return (f'Magazine "{self.name.title()}" was written by {self.author.title()},'
                f' magazine style is {self.style} and issued {self.issue_date}.')


# decorator for adding book
def add_book_decorator(func):
    @wraps(func)
    def inner(self, author, book, **kwargs):
        if author in self.book_dict.keys():
            if book in self.book_dict[author]:
                print('Such book is alredy in the library')
        else:
            print(f'\nNew book "{book}" was succesfully added to Library')
            return func(self, author, book, **kwargs)

    return inner


# decorator for deleting book
def del_book_decorator(func):
    @wraps(func)
    def inner(self, author, **kwargs):
        if author in self.book_dict.keys():
            print(f'\nBook "{self.book_dict[author]}" was succesfully deleted from Library')
            return func(self, author, **kwargs)
        else:
            print('Such book does no longer exist in the library')
    return inner


class Library:

    def __init__(self):
        # self.book_list = Book.book_list
        self.book_dict = Book.book_dict
        self.book_store = []

    def __iter__(self):
        self.__index = -1
        return self

    def __next__(self):
        self.__index += 1
        if self.__index < len(self.book_store):
            return self.book_store[self.__index]
        else:
            raise StopIteration

    def add_book(self, book: Book):
        self.book_store.append(book.__repr__())

    # eventually came up with how to implement method as generator
    def get_book_by_author(self, author):
        books = self.book_dict.get(author, [])
        for book in books:
            yield book

    def __getitem__(self, author):
        return self.book_dict.get(author, 'Wrong data, try again!!')

    # ТУТ не понял, ведь генератор вощврашает каждый следующий елемент, а как вернуть по имени автора?
    # Потому сделал выше ^ как смог через обычный словарь и __gettattr__
    # def __getitem__(self, item):
    #     res = iter((item[1] for item in self.book_dict.items()))
    #     return next(res)

    @del_book_decorator
    def __delitem__(self, key):
        del self.book_dict[key]
        print(self.book_dict)

    @add_book_decorator
    def __setitem__(self, author, book):
        # self.book_dict[author] = book
        self.book_dict.setdefault(author, []).append(book)
        print(self.book_dict)

    def __str__(self):
        return f'{[book for book in self.book_store]}'


# making BookModel instances
book_model_1 = BookModel(
    name='Harry Potter',
    author='J.K. Rowling',
    issue_date='08/09/1999',
)
book_model_2 = BookModel(
    name='It',
    author='Stephen King',
    issue_date='15/09/1986',
)
book_model_3 = BookModel(
    name='The Lord of the Rings',
    author='J.R.R. Tolkien',
    issue_date='29/07/1954',
)

book_model_4 = BookModel(
    name='Hobbit',
    author='J.R.R. Tolkien',
    issue_date='29/07/1954',
)

# displaying Book() instances
print(book1 := Book(book_model_1))
print(book2 := Book(book_model_2))
print(book3 := Book(book_model_3))
print(book4 := Book(book_model_4))

# iterator
library = Library()
library.add_book(book1)
library.add_book(book2)
library.add_book(book3)
library.add_book(book4)

same_author_books = library.get_book_by_author('J.R.R. Tolkien')
for lib_book in same_author_books:
    print('->', lib_book)

for i in library:
    print(i)

# just checking for myself if dict and list exist
print(library.book_store)
pprint(library.book_dict)

# returning name of book by author`s name
print(library['Stephen King'])
print(library['J.R.R. Tolkien'])
print(library['J.K. Rowling'])

# implemented del method for library
del library['Stephen King']

# implemented set method for library
library['Stephen King'] = 'It'

# context manager to wtite
with open('book_write_list.txt', 'w') as file_w:
    for author, book in library.book_dict.items():
        file_w.write(f'Book "{book}" by {author}\n')

print('\n')

# context manager to read
with open('book_write_list.txt', 'r') as file_r:
    book_list_from_file = [line.strip() for line in file_r.readlines()]
    pprint(book_list_from_file)

# inheritance
magazine_model = MagazineModel(
    name='Men`s health',
    author='Adam Campbell',
    issue_date='08/11/2003',
    style='health',
)

magazine = Magazine(magazine_model)
print(magazine)

header = 'Book Library'
print(f'{header:_^28s}:')
count = 0
for book in library:
    count += 1
    print(f'{count}{book:.>28s}')

library['Stephen King'] = 'It'  # --> Such book is alredy in the librery


