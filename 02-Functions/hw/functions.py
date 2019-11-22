import inspect
from collections import namedtuple


def letters_range(*args, **kwargs):
    """
    letters_range(stop) -> part of the alphabet
    letters_range(start, stop[, step, some_dict]) -> part of the alphabet

    Return an object that produces a sequence of symbols from start (inclusive)
    to stop (exclusive) by step. letters_range(g) produces 'a', 'b', 'c', 'd', 'e', 'f'.
    When step is given, it specifies the increment (or decrement).
    When some_dict is given, it replaces Latin alphabet with the specified symbols.
    letters_range('g', 'p', **{'l': 7, 'o': 0}) produces 'g', 'h', 'i', 'j', 'k', '7', 'm', 'n', '0'.
    """

    alphabet = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
        'w', 'x', 'y', 'z'
    ]
    new_args = {i: i for i in args}
    if kwargs:
        for i, letter in enumerate(alphabet):
            if letter in kwargs:
                alphabet[i] = (kwargs[letter])
            # taking in account boundary replaces
            if letter in args and letter in kwargs:
                new_args[letter] = kwargs[letter]

    indices = {letter: i for i, letter in enumerate(alphabet)}

    if len(args) == 1:
        start, stop, step = 'a', new_args[args[0]], 1
    elif len(args) == 2:
        start, stop, step = new_args[args[0]], new_args[args[1]], 1
    elif len(args) == 3:
        start, stop, step = new_args[args[0]], new_args[args[2]], args[2]
    else:
        raise TypeError('range expected at most 3 arguments, got 4')

    answer = alphabet[indices[start]:indices[stop]:step]

    return answer


def atom(arg=None):
    """
    :param arg: incoming argument
    :return: tuple of 4 functions: get_value, set_value, process_value, delete_value
    """

    # To provide functions call by their name outside the atom namedtuple is used
    Functions = namedtuple("Functions", 'get_value set_value process_value delete_value')

    def get_value():
        try:
            return arg
        except NameError:
            print("arg doesn't exist anymore")

    def set_value(new_val):
        nonlocal arg
        arg = new_val
        return arg

    def process_value(*funcs):
        nonlocal arg
        for foo in funcs:
            arg = foo(arg)
        return arg

    def delete_value():
        nonlocal arg
        del arg

    return Functions(get_value, set_value, process_value, delete_value)


def make_it_count(func, counter_name):
    """
    :param func: any function
    :param counter_name: counter of function calls
    :return: wrapper: new function behave exactly like func
    """

    def wrapper(*args, **kwargs):
        globals()[counter_name] += 1
        return func(*args, **kwargs)

    return wrapper


def modified_func(func, *fixated_args, **fixated_kwargs):
    def wrapper(*args, **kwargs):
        nonlocal fixated_args, fixated_kwargs
        fixated_args = (*fixated_args, *args)
        fixated_kwargs = {**fixated_kwargs, **kwargs}
        return func(*fixated_args, **fixated_kwargs)

    ans = inspect.getargvalues(inspect.currentframe())

    my_doc = f"""
             A func implementation of {func.__name__}
             with pre-applied arguments being:
             fixated_args: {ans.locals['fixated_args']};
             fixated_kwargs: {ans.locals['fixated_kwargs']};
             source_code: 
             {inspect.getsource(wrapper)}
             """
    wrapper.__doc__ = my_doc
    return wrapper


global_counter_name = 0


def main():
    pass

if __name__ == '__main__':
    main()
