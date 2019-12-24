"""
С помощью паттерна "Цепочка обязанностей" составьте список покупок для выпечки блинов.
Необходимо осмотреть холодильник и поочередно проверить, есть ли у нас необходимые ингридиенты:
    2 яйца
    300 грамм муки
    0.5 л молока
    100 грамм сахара
    10 мл подсолнечного масла
    120 грамм сливочного масла

В итоге мы должны получить список недостающих ингридиентов.
"""

from typing import Any, Optional
from abc import ABC, abstractmethod

EGGS = 2
FLOUR = 300
MILK = 0.5
SUGAR = 100
OIL = 10
BUTTER = 120


class Handler(ABC):
    """
    Интерфейс Обработчика объявляет метод построения цепочки обработчиков. Он
    также объявляет метод для выполнения запроса.
    """

    @abstractmethod
    def set_next(self, handler):
        pass

    @abstractmethod
    def handle(self, request) -> Optional[str]:
        pass


class AbstractHandler(Handler):
    """
    Поведение цепочки по умолчанию может быть реализовано внутри базового класса
    обработчика.
    """

    _next_handler: Handler = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        # Возврат обработчика отсюда позволит связать обработчики простым
        # способом, вот так:
        # handler1.set_next(handler2).set_next(handler3)
        return handler

    @abstractmethod
    def handle(self, request: Any) -> Optional[str]:
        if self._next_handler:
            return self._next_handler.handle(request)
        return None


class Refrigerator:
    def __init__(self, content):
        self.content = content


class EggsHandler(AbstractHandler):
    def handle(self, refrigerator):
        if refrigerator.content['eggs'] < EGGS:
            print(f"You need to add "
                  f"{EGGS - refrigerator.content['eggs']} eggs")
        if self._next_handler:
            return self._next_handler.handle(refrigerator)


class FlourHandler(AbstractHandler):
    def handle(self, refrigerator):
        if refrigerator.content['flour'] < FLOUR:
            print(f"You need to add {FLOUR - refrigerator.content['flour']}"
                  f" grams of flour")
        if self._next_handler:
            return self._next_handler.handle(refrigerator)


class MilkHandler(AbstractHandler):
    def handle(self, refrigerator):
        if refrigerator.content['milk'] < MILK:
            print(f"You need to add {MILK - refrigerator.content['milk']}"
                  f" l of milk")
        if self._next_handler:
            return self._next_handler.handle(refrigerator)


class SugarHandler(AbstractHandler):
    def handle(self, refrigerator):
        if refrigerator.content['sugar'] < SUGAR:
            print(f"You need to add {SUGAR - refrigerator.content['sugar']}"
                  f" grams of sugar")
        if self._next_handler:
            return self._next_handler.handle(refrigerator)


class OilHandler(AbstractHandler):
    def handle(self, refrigerator):
        if refrigerator.content['oil'] < OIL:
            print(f"You need to add {OIL - refrigerator.content['oil']}"
                  f" ml of oil")
        if self._next_handler:
            return self._next_handler.handle(refrigerator)


class ButterHandler(AbstractHandler):
    def handle(self, refrigerator):
        if refrigerator.content['butter'] < BUTTER:
            print(f"You need to add {BUTTER - refrigerator.content['butter']}"
                  f" grams of butter")
        if self._next_handler:
            return self._next_handler.handle(refrigerator)


if __name__ == '__main__':
    content = {'eggs': 1, 'flour': 200, 'milk': 1, 'sugar': 70, 'oil': 2,
               'butter': 119}
    refrigerator = Refrigerator(content)

    eggs_handler = EggsHandler()
    flour_handler = FlourHandler()
    milk_handler = MilkHandler()
    sugar_handler = SugarHandler()
    oil_handler = OilHandler()
    butter_handler = ButterHandler()

    eggs_handler.set_next(flour_handler).set_next(milk_handler).set_next(
        sugar_handler).set_next(oil_handler).set_next(butter_handler)

    eggs_handler.handle(refrigerator)
