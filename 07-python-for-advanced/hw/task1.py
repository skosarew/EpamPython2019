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


class SingletonMeta(type):
    _instances = {}
    _pool_keys = {}

    def __call__(cls, *args, **kwargs):
        def get_k_pool_key(args, kwargs):
            # print('args kwargs{', args, kwargs, '}\n\n')
            k = str(args) + ' ' + str(dict(sorted(kwargs.items(),
                                                  key=lambda x: x[0])))
            pool_key = tuple(list(args) + list(kwargs.values()))
            return k, pool_key

        k, pool_key = get_k_pool_key(args, kwargs)
        cls._pool_keys[pool_key] = k

        def connect_func(*args, **kwargs):
            # print(args, kwargs)
            pool_key = tuple(list(args) + list(kwargs.values()))
            return cls._instances[cls._pool_keys[pool_key]]

        # @classmethod
        def del_(instance):
            k, pool_key = get_k_pool_key(instance.args, instance.kwargs)
            if k in cls._instances:
                print('del key started', len(cls._instances))
                del cls._instances[k]
                # cls._instances['bbb'] = 111
                a = 1
                del a
                # del cls._instances['bbb']
                # print('del key finished', len(cls._instances))
                # cls._instances.pop(k)

            if pool_key in cls._pool_keys:
                print('del pool key started', len(cls._instances))
                del cls._pool_keys[pool_key]
                b = 1
                del b
                # cls._instances['ppp'] = 222
                # cls._pool_keys.pop(pool_key)
                # print('del pool key finished', len(cls._instances))

        if k not in cls._instances:
            instance = super(SingletonMeta, cls).__call__(*args, **kwargs)
            cls.__del__ = del_
            print('cls: ', cls)
            cls._instances[k] = instance
            print(cls._instances)
            # print('instances:', cls._instances)
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

    # unit22 = SiamObj('1', '2', b=1)
    # print('unit1 is unit2', unit1 is unit2)
    # print('unit1 is unit22', unit1 is unit22)

    unit3 = SiamObj('2', '2', a=1)
    print(sys.getrefcount(unit3))
    # print(unit3 is unit1)
    # unit1.a = 333
    # print('unit1.a', unit1.a, unit1.__dict__)

    # print('unit3.connect', unit3.connect('1', '2', 1))
    unit3.connect('1', '2', 1).a = 2
    # print('unit2.a == 2', unit2.a == 2)
    # print('unit2', unit2.__dict__)
    # print('unit3', unit3.__dict__)
    # print('pool', unit3.pool)
    pool = unit3.pool
    print('pool len init', len(pool))

    # print('unit3 del started')
    print(unit1.pool)
    del unit3
    print('pool len finish', len(pool))
    print(unit1.pool)
