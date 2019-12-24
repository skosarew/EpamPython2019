"""
Представьте, что вы пишите программу по формированию и выдачи комплексных обедов для сети столовых, которая стала
расширяться и теперь предлагает комплексные обеды для вегетарианцев, детей и любителей китайской кухни.

С помощью паттерна "Абстрактная фабрика" вам необходимо реализовать выдачу комплексного обеда, состоящего из трёх
позиций (первое, второе и напиток).
В файле menu.yml находится меню на каждый день, в котором указаны позиции и их принадлежность к
определенному типу блюд.
"""

from abc import ABC, abstractmethod
import yaml


class AbstractMeal(ABC):  # meal
    @abstractmethod
    def first(self) -> str:
        pass

    @abstractmethod
    def second(self) -> str:
        pass

    @abstractmethod
    def drink(self) -> str:
        pass


class ConcreteMealVegan(AbstractMeal):
    def first(self) -> str:
        return menu[today]['first_courses']['vegan']

    def second(self) -> str:
        return menu[today]['second_courses']['vegan']

    def drink(self) -> str:
        return menu[today]['drinks']['vegan']


class ConcreteMealChild(AbstractMeal):
    def first(self) -> str:
        return menu[today]['first_courses']['child']

    def second(self) -> str:
        return menu[today]['second_courses']['child']

    def drink(self) -> str:
        return menu[today]['drinks']['child']


class ConcreteMealChinese(AbstractMeal):
    def first(self) -> str:
        return menu[today]['first_courses']['chinese']

    def second(self) -> str:
        return menu[today]['second_courses']['chinese']

    def drink(self) -> str:
        return menu[today]['drinks']['chinese']


class AbstractFactory(ABC):
    @abstractmethod
    def create_meal(self) -> AbstractMeal:
        pass


class ConcreteFactoryVegan(AbstractFactory):
    def create_meal(self) -> ConcreteMealVegan:
        return ConcreteMealVegan()


class ConcreteFactoryChild(AbstractFactory):
    def create_meal(self) -> ConcreteMealChild:
        return ConcreteMealChild()


class ConcreteFactoryChinese(AbstractFactory):
    def create_meal(self) -> ConcreteMealChinese:
        return ConcreteMealChinese()


def client_code(factory: AbstractFactory) -> None:
    meal = factory.create_meal()
    first = meal.first()
    second = meal.second()
    drink = meal.drink()
    print(f"You ordered:\nfirst meal: {first},\nsecond meal: {second}"
          f"\ndrink: {drink}")


if __name__ == '__main__':
    with open("menu.yml", 'r') as stream:
        try:
            menu = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    today = input('Enter the day of the week:')

    print("Клиент: Тестируем код клиента с фабрикой веганов:")
    client_code(ConcreteFactoryVegan())

    print("\n")

    print("Клиент: Тестируем код клиента с фабрикой детей:")
    client_code(ConcreteFactoryChild())

    print("\n")

    print("Клиент: Тестируем код клиента с фабрикой китайской:")
    client_code(ConcreteFactoryChinese())
