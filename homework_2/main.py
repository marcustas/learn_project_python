from models import BookModel, MagazineModel
from library import Library
from constants import BOOKS, MAGAZINES

# створення бібліотеки
library = Library()

# створення інстансу книги та журналу
book_model_2 = BookModel(**BOOKS[0])
book_model_1 = BookModel(**BOOKS[1])
book_model_3 = BookModel(**BOOKS[2])
magazine_model_1 = MagazineModel(**MAGAZINES[0])
# додавання їх у бібліотеку
library.add_publication(book_model_2)
library.add_publication(book_model_1)
library.add_publication(book_model_3)
library.add_publication(magazine_model_1)
# виведення списку книг у бібліотеці
library.get_publication_list()

# виведення списку книг бібліотеки по імені автора
print('-----виведення списку книг бібліотеки по імені автора')
library.get_publication_by_author(book_model_1.author)

# збереження списку книг у файл
library.write_to_file()

# видалення книги з бібліотеки
print('-----виведення списку книг після видалення')
library.remove_publication(book_model_3)
library.remove_publication(book_model_1)
library.remove_publication(book_model_2)

# виведення списку книг після видалення
library.get_publication_list()

# додавання книг з файлу в бібліотеку
library.add_publications_from_file()

# виведення списку книг бібліотеки після додавання
print('-----виведення списку книг бібліотеки після додавання')
library.get_publication_list()
