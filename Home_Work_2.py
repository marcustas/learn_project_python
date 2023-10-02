from pydantic import BaseModel, field_validator
from pprint import pprint


class BookModel(BaseModel):
    name: str
    author: str
    issue_date: str

    @field_validator("issue_date")
    def validate_date(cls, value):
        if not isinstance(value, str):
            try:
                str(value)
            except Exception as e:
                print(e)
            else:
                return value


class Book():
    name = None
    author = None
    issue_date = None
    book_list = list()
    book_dict = dict()

    def __init__(self, book: BookModel):
        self.name = book.name
        self.author = book.author
        self.issue_date = book.issue_date
        self.book_list.append(self.__repr__())
        self.book_dict.setdefault(self.author, self.name)

    def __str__(self):
        return (f'Book "{self.name.title()}" was written by {self.author.title()} '
                f'and issued {self.issue_date}.')

    def __repr__(self):
        return f'{self.name.title()}'


# decorator for adding book
def add_book_decorator(func):
    def inner(self, *args, **kwargs):
        print(f'\nNew book "{args[1]}" was succesfully added to Library')
        return func(self, *args, **kwargs)

    return inner


# decorator for deleting book
def del_book_decorator(func):
    def inner(self, *args, **kwargs):
        if args[0] in self.book_dict.keys():
            print(f'\nBook "{self.book_dict[args[0]]}" was succesfully deleted from Library')
            return func(self, *args, **kwargs)

    return inner


class Library():
    index = -1

    def __init__(self):
        self.book_list = Book.book_list
        self.book_dict = Book.book_dict

    def __iter__(self):
        self.index = self.__class__.index
        return self

    def __next__(self):
        self.index += 1
        if self.index < len(self.book_list):
            return self.book_list[self.index]
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

    @add_book_decorator
    def __setitem__(self, author, book):
        self.book_dict[author] = book


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
pprint(library.book_dict)
del library['Stephen King']
print(library.book_dict)

# implemented set method for library
library['Stephen King'] = 'It'
print(library.book_dict)

with open('book_write_list.txt', 'w') as file:
    for author, book in library.book_dict.items():
        file.write(f'Book "{book}" by {author}\n')



# print(book.model_dump())
# pull, push, add branches, merge, merge_conflicts !!!   git checkout -b Test
