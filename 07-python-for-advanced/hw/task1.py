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

import sys
import weakref

class SingletonMeta(type):
    _instances = weakref.WeakValueDictionary()
    _pool_keys = {}

    def __call__(cls, *args, **kwargs):
        def get_k_pool_key(args, kwargs):
            k = str(args) + ' ' + str(dict(sorted(kwargs.items(),
                                                  key=lambda x: x[0])))
            pool_key = tuple(list(args) + list(kwargs.values()))
            return k, pool_key

        k, pool_key = get_k_pool_key(args, kwargs)
        cls._pool_keys[pool_key] = k

        def connect_func(*args, **kwargs):
            pool_key = tuple(list(args) + list(kwargs.values()))
            return cls._instances[cls._pool_keys[pool_key]]

        # @classmethod
        def custom_del(instance):
            k, pool_key = get_k_pool_key(instance.args, instance.kwargs)
            if k in cls._instances:
                del cls._instances[k]

            if pool_key in cls._pool_keys:
                del cls._pool_keys[pool_key]

        if k not in cls._instances:
            instance = super(SingletonMeta, cls).__call__(*args, **kwargs)
            cls.__del__ = custom_del
            cls._instances[k] = instance
            instance.connect = connect_func
            instance.pool = cls._instances
            return instance
        return cls._instances[k]


class SiamObj(metaclass=SingletonMeta):
    def __init__(self, *args, **kwargs):
        self.__dict__ = dict(kwargs)
        self.args = args
        self.kwargs = kwargs


if __name__ == '__main__':
    unit1 = SiamObj('1', '2', a=1)
    unit2 = SiamObj('1', '2', a=1)
    unit3 = SiamObj('2', '2', a=1)

    unit3.connect('1', '2', 1).a = 2
    pool = unit3.pool
    print('pool len init', len(pool))
    del unit3
    print('pool len finish', len(pool))
