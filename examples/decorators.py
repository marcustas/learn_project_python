import time


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f"Функція '{func.__name__}' виконувалася {elapsed_time:.4f} секунд")
        return result
    return wrapper


@timer
def long_running_function(num):
    for _ in range(num):
        pass


def run_decorated_func_without_args():
    long_running_function(1000000)


def logger(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        with open('log.txt', 'a') as file:
            file.write(
                f"Функція '{func.__name__}' була викликана з аргументами {args} і ключовими словами {kwargs}."
                f" Результат: {result}\n",
            )
        return result
    return wrapper


@logger
def add(a, b):
    return a + b


def run_decorated_func_with_args():
    add(2, 3)


if __name__ == '__main__':
    print('run_decorated_func_without_args')
    run_decorated_func_without_args()

    print('run_decorated_func_with_args()')
    run_decorated_func_with_args()
