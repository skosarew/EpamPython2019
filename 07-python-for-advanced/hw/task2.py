"""
Написать свое property c кэшем и таймаутом
полностью повторяет поведение стандартной property за исключением:
    * хранит результат работы метода некоторое время, которое передается
      параметром в инициализацию проперти
    * пересчитывает значение, если таймер истек
"""

import time
import datetime
import uuid


def timer_property(t):
    ttl = datetime.timedelta(seconds=t)

    """Caches the curr_time of function in memory with time to live"""

    class custom_property(object):
        def __init__(self, fget=None, fset=None, fdel=None, doc=None):
            self.fget = fget
            self.fset = fset
            self.fdel = fdel
            self.curr_time = 0
            self.result = 0
            if doc is None and fget is not None:
                doc = fget.__doc__
            self.__doc__ = doc

        def __get__(self, obj, objtype=None):
            if obj is None:
                return self
            if self.fget is None:
                raise AttributeError("unreadable attribute")
            if self.curr_time == 0 or \
                    datetime.datetime.now() - self.curr_time > ttl:
                self.result = self.fget(obj)
                self.curr_time = datetime.datetime.now()
            return self.result

        def __set__(self, obj, value):
            if self.fset is None:
                raise AttributeError("can't set attribute")
            self.curr_time = datetime.datetime.now()
            self.result = value

        def __delete__(self, obj):
            if self.fdel is None:
                raise AttributeError("can't delete attribute")
            self.fdel(obj)

        def getter(self, fget):
            return type(self)(fget, self.fset, self.fdel, self.__doc__)

        def setter(self, fset):
            return type(self)(self.fget, fset, self.fdel, self.__doc__)

        def deleter(self, fdel):
            return type(self)(self.fget, self.fset, fdel, self.__doc__)

    return custom_property


class Message:

    @timer_property(t=2)
    def msg(self):
        self._msg = self.get_message()
        return self._msg

    @msg.setter  # reset timer also
    def msg(self, param):
        self._msg = param

    def get_message(self):
        """
        Return random string
        """
        return uuid.uuid4().hex


if __name__ == '__main__':
    # m = Message()
    # initial = m.msg
    # assert initial is m.msg
    # time.sleep(2)
    # assert initial is not m.msg

    m = Message()
    m.msg = '12345qwerty'
    final = m.msg
    time.sleep(2.2)
    del m.msg
    print(m.msg)
    assert final is not m.msg