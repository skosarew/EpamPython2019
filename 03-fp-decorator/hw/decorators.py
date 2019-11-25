from functools import reduce
import time
import functools
from random import randint


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


import datetime


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

    # task 4
    passwords = ['Horus', 'Sanguinius', 'Horus', 'Dorn', 'Roboute', 'Horus']
    for password in passwords:
        print(slow_function(password))


if __name__ == '__main__':
    main()
