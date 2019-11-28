"""
Написать декоратор instances_counter, который применяется к любому классу
и добавляет ему 2 метода:
get_created_instances - возвращает количество созданых экземпляров класса
reset_instances_counter - сбросить счетчик экземпляров,
возвращает значение до сброса
Имя декоратора и методов не менять

Ниже пример использования
"""


def instances_counter(cls):
    """Adds get_created_instances and reset_instances_counter methods to cls"""

    cls._counter = 0

    def __new__(cls, *args, **kwargs):
        cls._counter += 1
        instance = super(cls, cls).__new__(cls)
        return instance

    @classmethod
    def get_created_instances(cls):
        return cls._counter

    @classmethod
    def reset_instances_counter(cls):
        old_counter = cls._counter
        cls._counter = 0
        return old_counter

    cls.get_created_instances = get_created_instances
    cls.reset_instances_counter = reset_instances_counter
    cls.__new__ = __new__
    return cls


@instances_counter
class User:
    pass


if __name__ == '__main__':
    print(User.get_created_instances())  # 0
    user, _, _ = User(), User(), User()
    print(user.get_created_instances())  # 3
    print(user.reset_instances_counter())  # 3

