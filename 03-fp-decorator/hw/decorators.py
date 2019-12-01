from __future__ import division
import time
import functools
import datetime
import math
from random import randint
from functools import reduce


def special_pythagorean_triplet():
    """
    a + b + c = 1000
    :return: a*b*c
    """
    return [a * b * (1000 - a - b) for a in range(1000 // 3) for b in
            range(a, 1000 // 2) if
            a * a + b * b == (1000 - a - b) * (1000 - a - b)][0]


def sum_square_difference():
    """Finds the difference between the sum of the squares of the first
    one hundred natural numbers and the square of the sum."""
    return sum([i for i in range(1, 101)]) ** 2 - sum(
        [i ** 2 for i in range(1, 101)])


def self_powers():
    """Finds the last ten digits of the series,
    1^1 + 2^2 + 3^3 + ... + 1000^1000.
    """
    return sum([i ** i for i in range(1, 1001)]) % (10 ** 10)


def champernownes_constant():
    """
    Finds the value of the following expression:
    d_1 × d_{10} × d_{100} × d_{1000} × d_{10000} × d_{100000} ×
    × d_{1000000}
    """
    return reduce(lambda x, y: int(x) * int(y),
                  [val for n, val in
                   enumerate("".join([str(i) for i in range(100000)]))
                   if n in (10 ** j for j in range(7))])


def is_armstrong(number):
    """Checks for Armstrong numbers"""
    return number == reduce(lambda x, y: x + y,
                            map(lambda x: int(x) ** len(str(number)),
                                str(number)))


def collatz_steps(n):
    return 0 if n == 1 else 1 + collatz_steps(
        n / 2) if n % 2 == 0 else 1 + collatz_steps(n * 3 + 1)


def make_cache(t):
    """Caches the results of function in memory with time to live"""
    results = {}
    ttl = datetime.timedelta(seconds=t)

    def decorator(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            key = tuple(args), frozenset(kwargs.items())
            if key not in results or \
                    datetime.datetime.now() - results[key][0] > ttl:
                result = func(*args, **kwargs)
                results[key] = (datetime.datetime.now(), result)
                print(f'New password for {key[0][0]}:')
                return result
            print(f'Password for {key[0][0]}:')
            return results[key][1]

        return inner

    return decorator


@make_cache(4)
def slow_function(*args, **kwargs):
    """
    Creates new passwords for users
    :param args:
    :param kwargs:
    :return: password
    """
    print('Password generation...')
    time.sleep(2)
    password = randint(1, 10)
    return password


def applydecorator(say_func):
    def wrapper1(foo_original):
        def wrapper2(*args, **kwargs):
            return say_func(foo_original, *args, **kwargs)

        return wrapper2

    return wrapper1


@applydecorator
def saymyname(f, *args, **kwargs):
    print('Name is', f.__name__)
    return f(*args, **kwargs)


# saymyname is now a decorator
@saymyname
def foo(*whatever):
    return whatever


global_counter1 = [0, 0]
global_counter2 = [0, 0]
global_counter3 = [0, 0]
global_counter4 = [0, 0]
global_counter5 = [0, 0]


def profiling_decorator_with_counter(counter_name):
    def profiling_decorator(func):
        def wrapper(*args, **kwargs):
            globals()[counter_name][0] += 1
            if globals()[counter_name][0] == 1:
                star_time = time.time()
                func_ans = func(*args, **kwargs)
                end_time = time.time() - star_time
                globals()[counter_name][1] += end_time
            else:
                func_ans = func(*args, **kwargs)

            return func_ans

        return wrapper

    return profiling_decorator


@profiling_decorator_with_counter('global_counter1')
def fib1(n):
    assert n >= 0
    return n if n <= 1 else fib1(n - 1) + fib1(n - 2)


cache = {}


@profiling_decorator_with_counter('global_counter2')
def fib2(n):
    assert n >= 0
    if n not in cache:
        cache[n] = n if n <= 1 else fib2(n - 1) + fib2(n - 2)
    return cache[n]


@profiling_decorator_with_counter('global_counter3')
def fib3(n):
    a = 0
    b = 1
    for __ in range(n):
        a, b = b, a + b
    return a


def custom_pow(x, n, I, mult):
    """
    Возвращает x в степени n. Предполагает, что I – это единичная матрица, которая
    перемножается с mult, а n – положительное целое
    """
    if n == 0:
        return I
    elif n == 1:
        return x
    else:
        y = custom_pow(x, n // 2, I, mult)
        y = mult(y, y)
        if n % 2:
            y = mult(x, y)
        return y


def identity_matrix(n):
    """Возвращает единичную матрицу n на n"""
    r = list(range(n))
    return [[1 if i == j else 0 for i in r] for j in r]


def matrix_multiply(A, B):
    bt = list(zip(*B))
    return [[sum(a * b
                 for a, b in zip(row_a, col_b))
             for col_b in bt]
            for row_a in A]


@profiling_decorator_with_counter('global_counter4')
def fib4(n):
    f = custom_pow([[1, 1], [1, 0]], n, identity_matrix(2), matrix_multiply)
    return f[0][1]


@profiling_decorator_with_counter('global_counter5')
def fib5(n):
    sqrt5 = math.sqrt(5)
    phi = (sqrt5 + 1) / 2
    return int(phi ** n / sqrt5 + 0.5)


def main():
    # task 1
    print(special_pythagorean_triplet())
    print(sum_square_difference())
    print(self_powers())
    print(champernownes_constant())

    # task 2
    assert is_armstrong(153) == True
    assert is_armstrong(10) == False

    # task 3
    assert collatz_steps(16) == 4
    assert collatz_steps(12) == 9
    assert collatz_steps(1000000) == 152

    # task (was deleted)
    passwords = ['Horus', 'Sanguinius', 'Horus', 'Dorn', 'Roboute', 'Horus']
    for password in passwords:
        print(slow_function(password))

    # task 4
    print(*foo(40, 2))

    # task 5
    fib1(30)
    print('recursion, global1: ', global_counter1)

    fib2(35)
    print('cache, global2: ', global_counter2)

    fib3(100000)
    print('dynamic, global3: ', global_counter3)

    fib4(100000)
    print('matrix, global4: ', global_counter4)

    fib5(1000)
    print('formula, global5: ', global_counter5)


if __name__ == '__main__':
    main()
