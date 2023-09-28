from contextlib import contextmanager


@contextmanager
def file_opener(filename, mode):
    file = open(filename, mode)
    yield file
    file.close()


class FileOpener:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()


def call_class_context_manager():
    with FileOpener('class_cm.txt', 'w') as file:
        file.write('Я був заповнений за допомогою классового контекстного менеджеру!')


def call_func_context_manager():
    with file_opener('func_cm.txt', 'w') as file:
        file.write('Я був заповнений за допомогою функціонального контекстного менеджеру!')


def call_try_finally_construction():
    file = None
    try:
        file = open('try_finally.txt', 'w')
        file.write('Я був заповнений за допомогою try/except/finally конструкцією!!')
    except Exception as e:
        print(f'Помилка: {e}')
    finally:
        if file:
            file.close()


if __name__ == '__main__':
    print('call_class_context_manager')
    call_class_context_manager()

    print('call_func_context_manager')
    call_func_context_manager()

    print('call_try_finally_construction')
    call_try_finally_construction()
