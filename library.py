from abc import ABC, abstractmethod

from pydantic import BaseModel


class BookModel(BaseModel):
    name: str
    author: str
    year: int


class JournalModel(BookModel):
    month: str


class AbstractPublication(ABC):
    @abstractmethod
    def display_info(self):
        raise NotImplementedError


class Book(AbstractPublication):
    def __init__(self, model: BookModel):
        self._model = model

    def __str__(self):
        return f"{self._model.name} by {self._model.author}, published in {self._model.year}"

    def display_info(self):
        return self.__str__()


class Journal(Book):
    def __init__(self, model: JournalModel):
        super().__init__(model)

    def __str__(self):
        return f"{self._model.name} by {self._model.author}, published in {self._model.year}"


def add_publication_log_decorator(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        print(f"Publication {args[1]._model.name} by {args[1]._model.author} was added to the library")

    return wrapper


def delete_and_print_decorator(func):
    def wrapper(*args, **kwargs):
        if args[1] not in args[0]._publications:
            print(f"Publication {args[1]._model.name} by {args[1]._model.author} is not in the library")
        else:
            func(*args, **kwargs)
            print(f"Publication {args[1]._model.name} by {args[1]._model.author} was deleted from the library")

    return wrapper


class FileOpener:
    def __init__(self, filename: str, mode: str):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()


class Library:
    def __init__(self):
        self._publications = []

    def __iter__(self):
        self.current_book = 0
        return self

    def __next__(self):
        if self.current_book >= len(self._publications):
            raise StopIteration

        book = self._publications[self.current_book]
        self.current_book += 1
        return book

    def get_publications_by_author(self, author: str):
        for book in self._publications:
            if book._model.author == author:
                yield book

    @add_publication_log_decorator
    def add_publication(self, publication: AbstractPublication):
        self._publications.append(publication)

    def add_publication_from_file(self, filename: str):
        with FileOpener(filename, "r") as file:
            for line in file:
                publication_data = line.split(", ")
                if len(publication_data) == 3:
                    self.add_publication(Book(BookModel(name=publication_data[0],
                                                        author=publication_data[1],
                                                        year=int(publication_data[2]))))
                elif len(publication_data) == 4:
                    self.add_publication(Journal(JournalModel(name=publication_data[0],
                                                              author=publication_data[1],
                                                              year=int(publication_data[2]),
                                                              month=publication_data[3].strip())))

    def write_publications_into_file(self):
        with FileOpener("books.txt", "w") as file:
            for publication in self._publications:
                if isinstance(publication, Book):
                    file.write(f"{publication._model.name}, {publication._model.author}, {publication._model.year}\n")
                elif isinstance(publication, Journal):
                    file.write(f"{publication._model.name}, {publication._model.author}, {publication._model.year}, "
                               f"{publication._model.month}\n")

    @delete_and_print_decorator
    def delete_publication(self, publication: AbstractPublication):
        self._publications.remove(publication)


if __name__ == "__main__":
    # Create library
    library = Library()
    print("1. Library has been created", end="\n\n")

    # Create publications
    publications = {
        "book 1": Book(BookModel(name="Book 1", author="Author 1", year=1980)),
        "book 2": Book(BookModel(name="Book 2", author="Author 1", year=1981)),
        "book 3": Book(BookModel(name="Book 3", author="Author 1", year=1982)),
        "book 4": Book(BookModel(name="Book 4", author="Author 2", year=1990)),
        "journal 1": Journal(JournalModel(name="Journal 1", author="Author 10", year=2023, month="October")),
        "journal 2": Journal(JournalModel(name="Journal 1", author="Author 10", year=2023, month="November")),
        "journal 3": Journal(JournalModel(name="Journal 1", author="Author 10", year=2023, month="December")),
        "journal 4": Journal(JournalModel(name="Journal 2", author="Author 11", year=2023, month="December")),
    }
    print("2. Publications have been created", end="\n\n")

    # Add publications into library
    for publication in publications.values():
        library.add_publication(publication)
    print("3. All publications have been added into library", end="\n\n")

    # Print all publications from library
    for publication in library:
        print(publication.display_info())
    print("4. All publications have been printed", end="\n\n")

    # Print all author books
    for publication in library.get_publications_by_author("Author 1"):
        print(publication)
    print("5. All \"Author 1\" books have been printed", end="\n\n")

    # Write publications into file
    library.write_publications_into_file()
    print("6. All publications have been written into \"books.txt\"", end="\n\n")

    # Delete all books (not journals) from library
    library.delete_publication(publications["book 1"])
    library.delete_publication(publications["book 2"])
    library.delete_publication(publications["book 3"])
    library.delete_publication(publications["book 4"])
    print("7. All books (not journals) have been deleted from library", end="\n\n")

    # Show all publications that remain after deletion
    for publication in library:
        print(publication.display_info())
    print("8. All publications that remain after deletion have been printed", end="\n\n")

    # Delete remaining publications
    library.delete_publication(publications["journal 1"])
    library.delete_publication(publications["journal 2"])
    library.delete_publication(publications["journal 3"])
    library.delete_publication(publications["journal 4"])
    print("All remaining publications have been deleted from library", end="\n\n")

    # Add publications from file
    library.add_publication_from_file("books.txt")
    print("9. Publications have been added from file", end="\n\n")

    # Print all publications from library
    for publication in library:
        print(publication.display_info())
    print("10. All publications have been printed", end="\n\n")
