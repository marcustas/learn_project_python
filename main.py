from contextlib import contextmanager
from lit_class import BookModel, MagazineModel
import csv


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
        for book in args[0].lit_list:
            if book.lib_id == args[1]:
                found = True
        assert found, "There are no books in the library with this id"
        result = func(*args, **kwargs)
        return result

    return wrapper


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


def author_books_gen(book_list: list, chosen_author: str):
    for book in book_list:
        if book.author == chosen_author:
            yield book


@contextmanager
def file_opener(filename: str, mode: str):
    """Opens the file in certain mode for further editing and closes it afterward"""
    csvfile = open(filename, mode)
    yield csvfile
    csvfile.close()


class Library:



    def __init__(self, from_file: str = None):
        self.lit_list = []
        self.book_iterator = BookIterator(self.lit_list)

    def show_books(self):
        print("\nHere are the books, currently present at the library and their library id's: ", end=' ')
        for book in self.book_iterator:
            print("\"" + book.title + "\"" + " (" + str(book.lib_id) + ")", end=", ")

    def show_ids(self):
        print("\nHere are the library ids, currently used: ", end=' ')
        for book in self.book_iterator:
            print(f"({book.lib_id})", end=", ")

    def show_author_books(self):
        print("\n")
        print(f"Here are the books written by {chosenAuthor}: ", end=" ")
        for book in author_books_gen(self.lit_list, chosenAuthor):
            print("\"" + book.title + "\"", end="; ")

    def write_with_context_manager(self):
        with file_opener('book_list.csv', 'w') as csvfile:
            w = csv.DictWriter(csvfile, MagazineModel.model_fields.keys())
            w.writeheader()
            books = list([b.model_dump() for b in self.lit_list])
            w.writerows(books)
            print("\nThe book list has successfully been updated")

    def read_with_context_manager(self):
        with file_opener('book_list.csv', 'r') as csvfile:
            csv_reader = csv.DictReader(csvfile, delimiter=',')
            self.lit_list.clear
            for row in csv_reader:
                if row['month'] == '':
                    l = BookModel(**row)
                else:
                    l = MagazineModel(**row)
                self.lit_list.append(l)

    @book_logger
    def add_book(self):
        with file_opener('book_list.csv', 'r') as csvfile:
            csv_reader = csv.DictReader(csvfile, delimiter=',')
            for row in csv_reader:
                if row['month'] == '':
                    l = BookModel(**row)
                else:
                    l = MagazineModel(**row)
                self.lit_list.append(l)
        lib.write_with_context_manager()
        print(f"\nThe new book \"{l.title}\" has successfully been added to the library.")

    @book_checker
    def book_remove(self, remove_id):
        for book in self.lit_list:
            if book.lib_id == remove_id:
                self.lit_list.remove(book)
                break
        lib.write_with_context_manager()
        print("\nChosen book has successfully been removed from the library. Here is the new list: ")
        lib.show_books()

if __name__=="__main__":
    initial_file_path = 'book_list.csv'
    edited_file_path = 'edited_bl.csv'
    lib = Library()

    lib.show_books()
    lib.read_with_context_manager()
    lib.show_author_books()
    # lib.write_with_context_manager()
    lib.book_remove(int(input("\nPlease, tell us the library id of the book you'd like to remove: ")))
    # lib.write_with_context_manager()
    # lib.add_book()
    # lib.show_books()
