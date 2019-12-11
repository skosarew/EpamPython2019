"""
Написать тесты(pytest or unittest) к предыдущим 2 заданиям, запустив которые, я бы смог бы проверить их корректность
Обязательно проверить всю критическую функциональность
"""

import unittest
from task2 import Message
from task1 import SiamObj
import time


class TestMessage(unittest.TestCase):
    def test_same_msg(self):
        """Returns True if msg is the same
        """
        m = Message()
        initial = m.msg
        self.assertEqual(initial, m.msg)

    def test_msg_with_delay(self):
        """Returns True if msg is not the same
        """
        m = Message()
        initial = m.msg
        time.sleep(2)
        self.assertNotEqual(initial, m.msg)

    def test_msg_with_small_delay(self):
        """Returns True if msg is not the same
        """
        m = Message()
        initial = m.msg
        time.sleep(1.9)
        self.assertEqual(initial, m.msg)

    def test_msg_set(self):
        """Returns True if msg is the same
        """
        m = Message()
        m.msg = '12345qwerty'
        final = m.msg
        # print(final, m.msg)
        self.assertEqual(final, m.msg)

    def test_msg_set_with_delay(self):
        """Returns True if msg is not the same
        """
        m = Message()
        m.msg = '12345qwerty'
        final = m.msg
        time.sleep(2)
        self.assertNotEqual(final, m.msg)


class TestMeta(unittest.TestCase):
    def test_siam_equal(self):
        """Returns True if objects with same arguments is the same
        """
        unit1 = SiamObj('1', '2', a=1)
        unit2 = SiamObj('1', '2', a=1)
        self.assertEqual(unit1, unit2)

    def test_siam_not_equal(self):
        """Returns True if objects with different args isn't the same
        """
        unit1 = SiamObj('1', '2', a=1)
        unit3 = SiamObj('2', '2', a=1)
        self.assertNotEqual(unit1, unit3)

    def test_siam_connections(self):
        """Returns True if object can access other objects
        of the same class
        """
        unit1 = SiamObj('1', '2', a=1)
        unit2 = SiamObj('1', '2', a=1)
        unit3 = SiamObj('2', '2', a=1)
        unit3.connect('1', '2', 1).a = 2
        self.assertEqual(2, unit1.a)
        self.assertEqual(2, unit2.a)

    def test_siam_deletion(self):
        """Return True if after deletion object the pool decreases by 1
        """
        unit1 = SiamObj('1', '2', a=1)
        unit2 = SiamObj('1', '2', a=1)
        unit3 = SiamObj('2', '2', a=1)
        pool = unit3.pool
        self.assertEqual(2, len(pool))
        del unit3
        self.assertEqual(1, len(pool))


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=3)
