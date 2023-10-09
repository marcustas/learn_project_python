from pydantic import BaseModel
from contextlib import contextmanager
from abc import ABC, abstractmethod

@contextmanager
def file_opener(filename: str, mode: str):
    file = open(filename, mode)
    yield file
    file.close()

class BookModel(BaseModel):
    book_name: str
    author: str
    year: int


class AbstractPublication(ABC):
    @abstractmethod
    def get_info(self):
        raise NotImplementedError

class Book(AbstractPublication):
    def __init__(self, model: BookModel):
        self._model = model
        self.book_name = model.book_name
        self.author = model.author
        self.year = model.year

    def __str__(self) -> str:
        return f"'{self._model.book_name}' {self._model.year} {self._model.author}"

    def __repr__(self) -> str:
        return self.__str__()

    def get_info(self) -> str:
        return f'Book title: {self._model.book_name}\nAuthor: {self._model.author}\nYear:{self._model.year}'


class Magazine(Book):
    def __init__(self, model: BookModel):
        super().__init__(model)

    def get_info(self) -> str:
        return f'Magazine title: {self._model.book_name}\nAuthor: {self._model.author}\nYear:{self._model.year}'


class Library:
    def __init__(self):
        self.book_collection = []

    def __iter__(self):
        self.current_book = 0
        return self

    def __next__(self):
        if self.current_book >= len(self.book_collection):
            raise StopIteration

        book = self.book_collection[self.current_book]
        self.current_book += 1
        return book

    def book_by_author_gen(self, author: str):
        return (book for book in self.book_collection if book.author == author)

    def save_data(self):
        with file_opener('library_list.txt', 'w') as file:
            for book in self.book_collection:
                file.write(f'{str(book)}\n')

    def load_data(self):
        with file_opener('library_list.txt', 'r') as file:
            return file.read().strip().split('\n')

    def logger(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open('log.txt', 'w', encoding='UTF-8') as file:
                file.write(f"Книга '{args[1].book_name}' була додана до бібліотеки.\n")
            return result
        return wrapper

    def is_exist(func):
        def wrapper(self, book):
            if book in self.book_collection:
                return func(self, book)
            else:
                print(f"Книги '{book.book_name}' не існує у бібліотеці")
        return wrapper

    @logger
    def add_book(self, book: Book):
        self.book_collection.append(book)


    def add_books(self, books: [Book]):
        for book in books:
            self.book_collection.append(book)

    @is_exist
    def del_book(self, book: Book):
        if book in self.book_collection:
            self.book_collection.remove(book)


# books_list = Library([book_1, book_2, book_3])
#
#
# not_existing_book_model = BookModel(book_name = 'Basdasad4', author = 'Unknown', year = 165436)
#
# books_list.add_book(new_book_model)
# books_list.add_book(mag_1)
#
# books_list.del_book(not_existing_book_model)
#
# books_list.save_data()
# books_list.load_data()

# print(*books_list, sep=',')

# Main code



Lib = Library() #creating a Library

# Creating models and inctances
book_model_1 = BookModel(book_name = 'Book1', author = 'Conan Doyle', year = 1256)
book_model_2 = BookModel(book_name = 'Book2', author = 'Johnathan Swift', year = 1956)
book_model_3 = BookModel(book_name = 'Book3', author = 'Anderson', year = 1656)

mag_model_1 = BookModel(book_name = 'Magazine', author = 'Johnathan Swift', year = 1656)
new_book_model = BookModel(book_name = 'Book4', author = 'Unknown', year = 1666)

book_1 = Book(book_model_1)
book_2 = Book(book_model_2)
book_3 = Book(book_model_3)

mag_1 = Magazine(mag_model_1)
new_book = Book(new_book_model)

Lib.add_books([book_1, book_2, book_3, mag_1]) #adding books to library

print(Lib.book_collection) #print all books in Library

print(*Lib.book_by_author_gen('Johnathan Swift'), sep=',') #print list of books by current author

Lib.save_data() #save data to file

Lib.del_book(book_2) #deleting a book

print(Lib.book_collection) #print all books in Library

loaded_data = Lib.load_data() #load data from file

Lib.add_books(loaded_data)

print('ss',Lib.book_collection) #print all books in Librar