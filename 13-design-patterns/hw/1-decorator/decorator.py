"""
Используя паттерн "Декоратор" реализуйте возможность дополнительно добавлять к кофе
    маршмеллоу, взбитые сливки и сироп, а затем вычислить итоговую стоимость напитка.
"""
from abc import ABC, abstractmethod


class Component(ABC):
    """
    Базовый интерфейс Компонента определяет поведение, которое изменяется декораторами.
    """

    @abstractmethod
    def get_cost(self):
        pass


class BaseCoffe(Component):
    def get_cost(self):
        return 90


class AbstractCoffeeDecorator(Component):
    def __init__(self, decorated_coffee):
        self.decorated_coffee = decorated_coffee

    def get_cost(self):
        return self.decorated_coffee.get_cost()


class Whip(AbstractCoffeeDecorator):
    def __init__(self, decorated_coffee):
        super(Whip, self).__init__(decorated_coffee)

    def get_cost(self):
        return self.decorated_coffee.get_cost() + 20


class Marshmallow(AbstractCoffeeDecorator):
    def __init__(self, decorated_coffee):
        super(Marshmallow, self).__init__(decorated_coffee)

    def get_cost(self):
        return self.decorated_coffee.get_cost() + 20


class Syrup(AbstractCoffeeDecorator):
    def __init__(self, decorated_coffee):
        super(Syrup, self).__init__(decorated_coffee)

    def get_cost(self):
        return self.decorated_coffee.get_cost() + 10


if __name__ == "__main__":
    coffe = BaseCoffe()
    coffe = Whip(coffe)
    coffe = Marshmallow(coffe)
    coffe = Syrup(coffe)
    print(f"Cтоимость чашки кофе: {str(coffe.get_cost())}")
