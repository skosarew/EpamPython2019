"""

Реализовать такой метакласс, что экземпляры класса созданного с помощью него
будут удовлетворять следующим требованиям:

* объекты созданные с одинаковыми аттрибутами будут одним и тем же объектом
* объекты созданные с разными аттрибутами будут разными объектами
* у любого объекта есть мозможность получить доступ к другим объектам
    того же класса


>>> unit1 = SiamObj('1', '2', a=1)
>>> unit2 = SiamObj('1', '2', a=1)
>>> unit1 is unit2
True
>>> unit3 = SiamObj('2', '2', a=1)
>>> unit3.connect('1', '2', 1).a = 2
>>> unit2.a == 2
True
>>> pool = unit3.pool
>>> print(len(pool))
2
>>> del unit3
>>> print(len(pool))
1

"""

import weakref


class MetaSiam(type):

    def __new__(mcs, *args, **kwargs):
        cls = super(MetaSiam, mcs).__new__(mcs, *args, **kwargs)
        cls._instances = weakref.WeakValueDictionary()
        cls._pool_keys = {}

        return cls

    def __call__(cls, *args, **kwargs):
        def get_k_pool_key(args, kwargs):
            args_kwargs_sorted = str(args) + ' ' + str(
                dict(sorted(kwargs.items(),
                            key=lambda x: x[0])))

            ordered_dict = dict(sorted(kwargs.items(), key=lambda x: x[0]))
            pool_key = tuple(list(args) + list(ordered_dict.values()))
            return args_kwargs_sorted, pool_key

        def connect_func(*args, **kwargs):
            args_kwargs_sorted, pool_key = get_k_pool_key(args, kwargs)
            return cls._instances[cls._pool_keys[pool_key], cls]

        def custom_del(instance):
            try:
                args_kwargs_sorted, pool_key = get_k_pool_key(instance.args,
                                                              instance.kwargs)
                if args_kwargs_sorted in cls._instances:
                    del cls._instances[args_kwargs_sorted]

                if pool_key in cls._pool_keys:
                    del cls._pool_keys[pool_key]
            except NameError:
                print("It's absent")

        args_kwargs_sorted, pool_key = get_k_pool_key(args, kwargs)

        if args_kwargs_sorted not in cls._pool_keys.values():
            cls._pool_keys[pool_key] = args_kwargs_sorted

        if (args_kwargs_sorted, cls) not in cls._instances:
            instance = super(MetaSiam, cls).__call__(*args, **kwargs)
            cls._instances[(args_kwargs_sorted, cls)] = instance
            cls.__del__ = custom_del
            instance.connect = connect_func
            instance.pool = cls._instances
            return instance
        return cls._instances[(args_kwargs_sorted, cls)]


class SiamObj(metaclass=MetaSiam):
    def __init__(self, *args, **kwargs):
        self.__dict__ = dict(kwargs)
        self.args = args
        self.kwargs = kwargs
class SiamSubj(metaclass=MetaSiam):
    def __init__(self, *args, **kwargs):
        self.__dict__ = dict(kwargs)
        self.args = args
        self.kwargs = kwargs


if __name__ == '__main__':
    unit0 = SiamObj()
    unit1 = SiamObj('1', '2', a=1, b=3, c=10)
    unit2 = SiamObj('1', '2', b=3, c=10, a=1)
    unit3 = SiamObj('2', '2', a=0, b=33)

    pool = unit3.pool
    print('pool len init', len(pool))
    del unit3
    del unit0

    print('pool len finish', len(pool))
    unit6 = SiamObj('1', '1', a=0, b=33)
