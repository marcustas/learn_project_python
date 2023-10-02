from pydantic import BaseModel
from pprint import pprint
from abc import ABC, abstractmethod
from functools import wraps


class BookModel(BaseModel):
    name: str
    author: str
    issue_date: str


class AbstractClass(ABC):
    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def __str__(self):
        raise NotImplementedError


class Book(AbstractClass):
    name = None
    __author = None
    issue_date = None
    book_list = list()
    book_dict = dict()

    def __init__(self, book: BookModel):
        self.name = book.name
        self.__author = book.author
        self.issue_date = book.issue_date
        self.book_list.append(self.__repr__())  # При создании каждого обьекта закидываю его в список
        self.book_dict.setdefault(self.__author, self.name)  # Тоже самое но в дикт

    def __str__(self):
        return (f'Book "{self.name.title()}" was written by {self.__author.title()} '
                f'and issued {self.issue_date}.')

    def __repr__(self):
        return f'{self.name.title()}'


class Magazine(Book):

    def __init__(self, book: BookModel, style):
        super().__init__(book)
        self.style = style

    def __str__(self):
        return (f'Magazine "{self.name.title()}" was written by {self.__author.title()},'
                f' magazine style is {self.style} and issued {self.issue_date}.')


# decorator for adding book
def add_book_decorator(func):
    @wraps(func)
    def inner(self, *args, **kwargs):
        print(f'\nNew book "{args[1]}" was succesfully added to Library')
        return func(self, *args, **kwargs)

    return inner


# decorator for deleting book
def del_book_decorator(func):
    @wraps(func)
    def inner(self, *args, **kwargs):
        if args[0] in self.book_dict.keys():
            print(f'\nBook "{self.book_dict[args[0]]}" was succesfully deleted from Library')
            return func(self, *args, **kwargs)

    return inner


class Library():

    def __init__(self):
        self.book_list = Book.book_list
        self.book_dict = Book.book_dict

    def __iter__(self):
        self.__index = -1
        return self

    def __next__(self):
        self.__index += 1
        if self.__index < len(self.book_list):
            return self.book_list[self.__index]
        else:
            raise StopIteration

    def __getitem__(self, item):
        return self.book_dict.get(item, 'Wrong data, try again!!')

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
        self.book_dict[author] = book
        print(self.book_dict)


# making BookModel instances
book_model_1 = BookModel(
    name='Harry Potter',
    author='J.K. Rowling',
    issue_date='08/09/1999'
)
book_model_2 = BookModel(
    name='it',
    author='Stephen King',
    issue_date='15/09/1986'
)
book_model_3 = BookModel(
    name='The Lord of the Rings',
    author='J.R.R. Tolkien',
    issue_date='29/07/1954'
)

# displaying Book() instances
print(book1 := Book(book_model_1))
print(book2 := Book(book_model_2))
print(book3 := Book(book_model_3))

# iterator
library = Library()
for i in library:
    print(i)

# just checking for myself if dict and list exist
print(library.book_list)
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
magazine_model = BookModel(
    name='Men`s health',
    author='Adam Campbell',
    issue_date='08/11/2003'
)

magazine = Magazine(magazine_model, 'health')


