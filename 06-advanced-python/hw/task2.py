"""
Реализовать класс Quaternion, позволяющий работать с кватернионами
https://ru.wikipedia.org/wiki/%D0%9A%D0%B2%D0%B0%D1%82%D0%B5%D1%80%D0%BD%D0%B8%D0%BE%D0%BD
Функциональность (магическими методами):
- сложение
- умножение
- деление
- сравнение
- нахождение модуля
- строковое представление и repr
По желанию:
- взаимодействие с числами других типов
"""


class Quaternion:
    """
    Class represents a four-dimensional associative normed division
    algebra over the real numbers.
    Represented in the form: a + bi + cj + dk
    """

    def __init__(self, a=0, b=0, c=0, d=0):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def __add__(self, other):
        if isinstance(other, Quaternion):
            return Quaternion(
                a=self.a + other.a, b=self.b + other.b, c=self.c + other.c,
                d=self.d + other.d)
        if isinstance(other, (int, float)):
            return self + Quaternion(other)

    def __iadd__(self, other):
        return self + other

    def __radd__(self, other):
        return self + other

    def __mul__(self, other):
        if isinstance(other, Quaternion):
            uv = self.dot_product(other)
            av = [self.a * other.b, self.a * other.c, self.a * other.d]
            bu = [other.a * self.b, other.a * self.c, other.a * self.d]
            u_v = self.cross_product(other)

            calc = [x + y + z for x, y, z in list(zip(av, bu, u_v))]
            return Quaternion(a=self.a * other.a - uv, b=calc[0], c=calc[1],
                              d=calc[2])
        if isinstance(other, (int, float)):
            return self * Quaternion(other)

    def __imul__(self, other):
        return self * other

    def __rmul__(self, other):
        return Quaternion(other) * self

    def __truediv__(self, other):
        if isinstance(other, Quaternion):
            return self * other.inverse()
        if isinstance(other, (int, float)):
            return self / Quaternion(other)

    def __rtruediv__(self, other):
        return Quaternion(other) * self.inverse()

    def __eq__(self, other):
        if isinstance(other, Quaternion):
            return self.__abs__() == other.__abs__()
        if isinstance(other, (int, float)):
            return self.__eq__(Quaternion(other))

    def __abs__(self):
        return self.sum_of_squares() ** (1 / 2)

    def __str__(self):
        return f'{self.a:.3f} {self.b:+.3f}i {self.c:+.3f}j ' \
            f'{self.d:+.3f}k'

    def __repr__(self):
        return f'Quaternion({repr(self.a)}, {repr(self.b)}, {repr(self.c)}, ' \
            f'{repr(self.d)})'

    def dot_product(self, other):
        return self.b * other.b + self.c * other.c + self.d * other.d

    def cross_product(self, other):
        return [self.c * other.d - self.d * other.c, self.d * other.b -
                self.b * other.d, self.b * other.c - self.c * other.b]

    def sum_of_squares(self):
        return self.a ** 2 + self.b ** 2 + self.c ** 2 + self.d ** 2

    def vector_conjugate(self):
        return Quaternion(a=self.a, b=-self.b, c=-self.c, d=-self.d)

    def inverse(self):
        ss = self.sum_of_squares()
        if ss > 0:
            conj_vector = self.vector_conjugate()
            return Quaternion(a=conj_vector.a / ss, b=conj_vector.b / ss,
                              c=conj_vector.c / ss, d=conj_vector.d / ss)
        else:
            raise ZeroDivisionError(
                "can't invert a zero quaternion")
