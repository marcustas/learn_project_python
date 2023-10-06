from contextlib import contextmanager
import lit_class
from book_list import lit_list


def book_logger(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print("\n-LOG: The book has successfully been added to the library")
        with open('log.txt', 'a') as file:
            file.write(
                f"Function '{func.__name__}' has been called."
                f"{result}",
            )
        return result

    return wrapper


def book_checker(func):
    def wrapper(*args, **kwargs):
        found = False
        for book in lit_list:
            if book.lib_id == args[0]:
                found = True
        assert found, "There are no books in the library with this id"
        result = func(*args, **kwargs)
        return result

    return wrapper


# rp_book = lit_class.BookModel(title="Roadside Picnic", author="Arkady and Boris Strugatsky", year=1971, lib_id=1)
# pfe_book = lit_class.BookModel(title="Python for Everybody: Exploring data using Python3", author="Charles Severance", year=2016, lib_id=2)
# hpp_book = lit_class.BookModel(title="Harry Potter and the Prisoner of Azkaban", author="J.K. Rowling", year=1999, lib_id=3)
# hph_book = lit_class.BookModel(title="Harry Potter and the Half-Blood Prince", author="J.K. Rowling", year=2005, lib_id=4)
# bb_magazine = lit_class.BookModel(title="Bloomberg Businessweek", author="Ashlee Vance", year=2016, month="December", type="Business", lib_id=5)
# ng_magazine = lit_class.BookModel(title="National Geographic", author="Andrew Evans", year=1999, month="November", type="Nature", lib_id=6)
#
# lit_list = [rp_book, pfe_book, hpp_book, hph_book, bb_magazine, ng_magazine]

# chosenAuthor = str(input("What author's books would you like to see?"))
chosenAuthor = "J.K. Rowling"


class BookIterator:
    def __init__(self, book_list: list):
        self.books = book_list

    def __iter__(self):
        self.book_index = 0
        return self

    def __next__(self):
        if self.book_index < len(self.books):
            book = self.books[self.book_index]
            self.book_index += 1
            return book
        raise StopIteration


book_iterator = BookIterator(lit_list)


def author_books_gen(book_list: list, chosen_author: str):
    for book in book_list:
        if book.author == chosen_author:
            yield book


def make_book():
    type_check = str(input(
        "\n Would you like to add a book or a magazine? "
        "(Write \"Book\" to add a book, write \"Magazine\" to add a book): "))
    lib.show_ids()

    if type_check.lower() == "book":
        lit_output = lit_class.BookModel(title=str(input("\nPlease, enter the book's title: ")),
                                         author=str(input("Please, enter the book's author: ")),
                                         year=int(input("Please, enter the year when the book was written: ")),
                                         lib_id=int(input("Create a library id for your book (The id can't be repeated or be < 0): "))
                                         )

    elif type_check.lower() == "magazine":
        lit_output = lit_class.MagazineModel(title=str(input("\nPlease, enter the magazine's title: ")),
                                             author=str(input("Please, enter the magazine's main author: ")),
                                             month=str(input("Please, enter the month when the journal was published: ")),
                                             type=str(input("Please, enter the type of Journal: ")),
                                             year=int(input("Please, enter the year when the magazine was published: ")),
                                             lib_id=int(input("Create a library id for your magazine (The id can't be repeated): "))
                                             )
    else:
        return None

    return lit_output


@contextmanager
def file_opener(filename: str, mode: str):
    """Opens the file in certain mode for further editing and closes it afterward"""
    file = open(filename, mode)
    yield file
    file.close()


def call_func_context_manager():
    with file_opener('book_list.txt', 'w') as file:
        file.write("Here is the book list: ")
        for book in lit_list:
            file.write("\"" + book.title + "\"" + "; ")
        print("The files has successfully been changed")


class Library:

    def show_books(self):
        print("\nHere are the books, currently present at the library and their library id's: ", end=' ')
        for book in book_iterator:
            print("\"" + book.title + "\"" + " (" + str(book.lib_id) + ")", end=", ")

    def show_ids(self):
        print("\nHere are the library ids, currently used: ", end=' ')
        for book in book_iterator:
            print(f"({book.lib_id})", end=", ")

    def show_author_books(self):
        print("\n")
        print(f"Here are the books written by {chosenAuthor}: ", end=" ")
        for book in author_books_gen(lit_list, chosenAuthor):
            print("\"" + book.title + "\"", end="; ")

    @book_logger
    def add_book(self, lit_output):
        assert lit_output is not None, "This book is None"
        found = False
        for book in lit_list:
            if book.lib_id == lit_output.lib_id:
                found = True
                break
        assert not found, "You're trying to create a book with the existing library id"
        lit_list.append(lit_output)
        print(f"\nYour book \"{lit_output.title}\" has successfully been added to the library.")

    @book_checker
    def book_remove(self, remove_id):
        for book in lit_list:
            if book.lib_id == remove_id:
                lit_list.remove(book)
                break

        print("\nYour book has successfully been removed from the library. Here is the new list: ")
        lib.show_books()


lib = Library()

lib.show_books()
lib.show_author_books()
# call_func_context_manager()
lib.show_books()
lib.book_remove(int(input("\nPlease, tell us the library id of the book you'd like to remove: ")))
lib.add_book(make_book())
lib.show_books()

