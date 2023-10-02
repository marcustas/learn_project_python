from examples.constants import MOVIES


def movie_generator():
    for movie in MOVIES:
        yield movie


def via_for_loop():
    for movie in movie_generator():
        print(movie)


def use_generator_expression():
    movie_gen = (title for title in MOVIES)

    for movie in movie_gen:
        print(movie)


def use_next():
    movie_gen = (title.upper() for title in MOVIES)
    print(next(movie_gen))  # Виведе "Фільм: Шерлок Голмс"


def second_generator_usage():
    movie_gen = (title for title in MOVIES)

    # Використовуємо генератор вперше
    for movie in movie_gen:
        print(movie)

    print('Спроба викликати генератор вдруге:')

    # Спроба використовувати генератор вдруге
    for movie in movie_gen:
        print(movie)


if __name__ == '__main__':
    print('via_for_loop')
    via_for_loop()

    print('use_generator_expression')
    use_generator_expression()

    print('use_next')
    use_next()

    print('second_generator_usage')
    second_generator_usage()
