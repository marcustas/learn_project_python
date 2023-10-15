from publications import Book, Magazine
from library import Library
from models import BookModel, MagazineModel

if __name__ == '__main__':
    library = Library()

    book_model1 = BookModel(name='Rich Dad Poor Dad', author='Robert Kiyosaki', year_of_publish=1997)
    book_model2 = BookModel(name='Your Money Or Your Life', author='Joseph R. Dominguez', year_of_publish=1992)
    book_model3 = BookModel(name='Rich Dads Cashflow Quadrant', author='Robert Kiyosaki', year_of_publish=1998)
    book_model4 = BookModel(name='Test', author='Test', year_of_publish=1995)
    my_book1 = Book(book_model1)
    my_book2 = Book(book_model2)
    my_book3 = Book(book_model3)
    my_book4 = Book(book_model4)
    print(my_book1.display_info())
    print(my_book2.display_info())
    print(my_book3.display_info())

    magazine_model1 = MagazineModel(name='Cool', author='N/A', year_of_publish=1990, month=1)
    magazine_model2 = MagazineModel(name='Cool', author='N/A', year_of_publish=1990, month=2)
    my_magazine1 = Magazine(magazine_model1)
    my_magazine2 = Magazine(magazine_model2)
    print(my_magazine1.display_info())
    print(my_magazine2.display_info())

    library.add_book_to_library(my_book1)
    library.add_book_to_library(my_book2)
    library.add_book_to_library(my_book3)
    library.add_book_to_library(my_magazine1)
    library.add_book_to_library(my_magazine2)

    library.get_books_from_library()

    library.iterate_books()
    for book in library.get_books_from_library_by_author("Robert Kiyosaki"):
        print(book)

    library.write_library_to_file('library.txt')

    library.delete_book_from_library(my_book2)
    library.delete_book_from_library(my_book4)

    library2 = Library()
    loaded_publications = library2.read_library_from_file('library.txt')
    library2.get_books_from_library()
