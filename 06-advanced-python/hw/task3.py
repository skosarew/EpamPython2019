""""
Реализовать контекстный менеджер, который подавляет переданные исключения
with Suppressor(ZeroDivisionError):
    1/0
print("It's fine")
"""


class Suppressor:
    """
    Suppress given exceptions.
    """

    def __init__(self, *errors):
        self.errors = errors

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f'exit exception text: {exc_val}')
        if exc_type in self.errors:
            return True


if __name__ == '__main__':
    with Suppressor(ZeroDivisionError, TypeError):
        1 / 0
    print("It's fine")
