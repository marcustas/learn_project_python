from lit_class import BookModel, MagazineModel

lit_list = [
    BookModel(title="Roadside Picnic", author="Arkady and Boris Strugatsky", year=1971, lib_id=1),
    BookModel(title="Python for Everybody: Exploring data using Python3", author="Charles Severance", year=2016, lib_id=2),
    BookModel(title="Harry Potter and the Prisoner of Azkaban", author="J.K. Rowling", year=1999, lib_id=3),
    BookModel(title="Harry Potter and the Half-Blood Prince", author="J.K. Rowling", year=2005, lib_id=4),
    MagazineModel(title="Bloomberg Businessweek", author="Ashlee Vance", year=2016, month="December", type="Business", lib_id=5),
    MagazineModel(title="National Geographic", author="Andrew Evans", year=1999, month="November", type="Nature", lib_id=6),
]