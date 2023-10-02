from pydantic import BaseModel, field_validator


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

    def __init__(self, book: BookModel):
        self.name = book.name
        self.author = book.author
        self.issue_date = book.issue_date
        self.book_list.append(self.__repr__())

    def __str__(self):
        return (f'Book "{self.name.title()}" was written by {self.author.title()} '
                f'and issued {self.issue_date}.')

    def __repr__(self):
        return f'{self.name.title()}'


class Library():
    index = -1

    def __init__(self):
        self.book_list = Book.book_list

    def __iter__(self):
        self.index = self.__class__.index
        return self

    def __next__(self):
        self.index += 1
        if self.index < len(self.book_list):
            return self.book_list[self.index]
        else:
            raise StopIteration




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


print()
library = Library()
print(library.book_list)
for i in library:
    print(i)



# print(book.model_dump())
# pull, push, add branches, merge, merge_conflicts !!!   git checkout -b Test
