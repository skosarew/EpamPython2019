"""
Написать декоратор который позволит сохранять информацию из
исходной функции (__name__ and __doc__), а так же сохранит саму
исходную функцию в атрибуте __original_func

print_result изменять нельзя, за исключением добавления вашего
декоратора на строку отведенную под него - замените комментарий

До применения вашего декоратор будет вызываться AttributeError при custom_sum.__original_func
Это корректное поведение
После применения там должна быть исходная функция

Ожидаемый результат:
print(custom_sum.__doc__)  # 'This function can sum any objects which have __add___'
print(custom_sum.__name__)  # 'custom_sum'
print(custom_sum.__original_func)  # <function custom_sum at <some_id>>
"""

import functools


def check_with_class(original_func):
    """
    Realization based on class.
    :param original_func:
    """

    class MyDec:
        def __init__(self, original_func):
            self.func = original_func

        def __call__(self, *args, **kwargs):
            self.__name__ = original_func.__name__
            self.__doc__ = original_func.__doc__
            self.__original_func = original_func
            self.func(*args, **kwargs)

    return MyDec


def check(original_func):
    def decorator(func):
        @functools.wraps(original_func)
        def inner(*args, **kwargs):
            return func(*args, **kwargs)

        inner.__original_func = original_func
        return inner

    return decorator


def print_result(func):
    @check(func)
    def wrapper(*args, **kwargs):
        """Function-wrapper which print result of an original function"""
        result = func(*args, **kwargs)
        print(result)
        return result

    return wrapper


@print_result
def custom_sum(*args):
    """This function can sum any objects which have __add___"""
    return functools.reduce(lambda x, y: x + y, args)


if __name__ == '__main__':
    custom_sum([1, 2, 3], [4, 5])
    custom_sum(1, 2, 3, 4)

    print(custom_sum.__doc__)
    print(custom_sum.__name__)
    without_print = custom_sum.__original_func

    # the result returns without printing
    without_print(1, 2, 3, 4)

    # replace decorator with @check_with_class(func)
    # without_print2 = custom_sum._MyDec.__original_func
    # without_print2(1, 2, 3, 4)
