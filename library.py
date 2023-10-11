from pydantic import BaseModel
from abc import ABC, abstractmethod

class Publication(ABC):
    @abstractmethod
    def get_title(self):
        pass

    @abstractmethod
    def get_autor(self):
        pass

    @abstractmethod
    def get_year(self):
        pass
class Bookmodel(BaseModel):
    title: str
    year: int
    autor: str


class Book(Publication):
    def __init__(self,title,year,autor):
        self.__title=title
        self.__year=year
        self.__autor=autor

    def __str__(self):
        return Book(f'{self.title} by {self.autor} from {self.year}')

class Library:
    def __init__(self):
        self.books=[]

    def __iter__(self):
        return iter(self.books)
    def generator_books(self,autor: str):
        for book in self.books:
            if book.autor == autor:
                yield book

    def log_add_book(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            print("New book added to the library!")
            return result
        return wrapper

    @log_add_book
    def add_book(self, book: Book):
        self.books.append(book)

    def check_del_book(func):
        def wrapper(self,book):
            if book in self.books:
                print('this book exist in library')
            return func(self,book)
        return wrapper
    @check_del_book
    def dell_book(library,book):
        library.books.remove(book)

    def save_file(self, file_name: str):
        with open(file_name,'w') as file:
            for book in self.books:
                file.write(f'{book.title},{book.autor},{book.year}\n')

    def load_book(self,file_name:str):
        with open(file_name, 'r') as file:
            for new_book in file.readlines():
                title, autor, year = new_book.strip().split(",")
                self.books.append(Bookmodel(title=title, autor=autor, year=int(year)))

class Magazine(Bookmodel):
    pass

library=Library()
book1=Bookmodel(title='Harry Potter 1',autor='J.K.Rowling',year='1997')
book2=Bookmodel(title='Harry Potter 2',autor='J.K.Rowling',year='1998')
book3=Bookmodel(title='Harry Potter 3',autor='J.K.Rowling',year='1999')
magazine1=Magazine(title='Football',autor='A.Frankow',year='2005')
print('створення бібліотеки')
library.books.append(book1)
library.books.append(book2)
library.books.append(book3)
library.books.append(magazine1)

for book in library:
    print(book)
print('виведення списку книг бібліотеки по імені автора')
for book in library.generator_books("A.Frankow"):
    print(book)

library.add_book(Bookmodel(title='The Catcher in the Rye', autor='J.D. Salinger', year=1951))
print(library.books)

# #збереження списку книг у файл
library.save_file("books.txt")
# видалення книги з бібліотеки
library.dell_book(book2)
print(library.books)
# # додавання книг з файлу в бібліотеку

library.load_book('books.txt')

print("виведення списку книг бібліотеки після додавання")
for book in library:
    print(book)

