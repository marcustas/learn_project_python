"""
Ітератори в Python - це об'єкти, які реалізують два методи: __iter__() та __next__().
Ітератори дозволяють ітерувати (або проходитися) по елементам колекції (наприклад, списку або словника) послідовно.
"""
from examples.constants import MOVIES


class MovieCollection:
    def __init__(self, movies_list: list[str] = MOVIES):
        self.movies = movies_list

    def __iter__(self):
        self.current_movie = 0
        return self

    def __next__(self):
        if self.current_movie >= len(self.movies):
            raise StopIteration

        movie = self.movies[self.current_movie]
        self.current_movie += 1
        return movie


my_movies = MovieCollection()


def iter_movies_with_function(movies: MovieCollection = my_movies):
    movie_iterator = iter(movies)

    print(next(movie_iterator))  # Фільм 1: Шерлок Голмс
    print(next(movie_iterator))  # Фільм 2: Інцепція
    print(next(movie_iterator))  # Фільм 3: Матриця

    # Цей наступний виклик спричинить StopIteration, тому що всі фільми вже були перебрані.
    print(next(movie_iterator))


def iter_movies_with_magic_methods(movies: MovieCollection = my_movies):
    movie_iterator = movies.__iter__()

    print(movie_iterator.__next__())  # Фільм 1: Шерлок Голмс
    print(movie_iterator.__next__())  # Фільм 2: Інцепція


def iter_via_for_loop(movies: MovieCollection):
    for movie in movies:
        print(movie)


if __name__ == '__main__':
    print('iter_movies_with_function')
    iter_movies_with_function()

    print('iter_movies_with_magic_methods')
    iter_movies_with_magic_methods()

    print('iter_via_for_loop')
    iter_via_for_loop(movies=MOVIES)
