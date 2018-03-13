import unittest
from datetime import datetime, timedelta
from types import GeneratorType

from giammis.utils.gdatetime import xrange_datetime


class XRangeDatetimeTest(unittest.TestCase):
    def test_generator_type(self):
        start = datetime(2017, 1, 1)
        end = datetime(2017, 1, 2)
        delta = timedelta(hours=1)
        space = xrange_datetime(start, end, delta)
        self.assertIsInstance(space, GeneratorType)
        pass

    def test_length_simple(self):
        start = datetime(2017, 1, 1)
        end = datetime(2017, 1, 2)
        delta = timedelta(hours=1)
        space = xrange_datetime(start, end, delta)
        # First time is 24
        length = len([x for x in space])
        expected = 24
        self.assertEqual(length, expected)
        # Second time is 0
        length = len([x for x in space])
        expected = 0
        self.assertEqual(length, expected)
        pass

    def test_elements_simple(self):
        start = datetime(2017, 1, 1)
        end = datetime(2017, 1, 2)
        delta = timedelta(hours=1)
        space = xrange_datetime(start, end, delta)
        current = start
        for elem in space:
            self.assertEqual(elem, current)
            current += delta
        pass

    def test_elements_hard(self):
        start = datetime(2017, 1, 1)
        end = datetime(2017, 1, 12)
        delta = timedelta(seconds=60 * 30)  # half an hour
        space = xrange_datetime(start, end, delta)
        current = start
        count = 0
        for elem in space:
            self.assertEqual(elem, current)
            count += 1
            current += delta
        count_expected = 11 * 24 * 2
        self.assertEqual(count, count_expected)
        pass

    def test_elements_hard_shift(self):
        start = datetime(2017, 1, 1, 6, 0)  # Shift A start
        end = datetime(2017, 1, 2, 14, 0)  # Shift A end day after
        delta = timedelta(hours=8)  # shift length
        space = xrange_datetime(start, end, delta)
        current = start
        count = 0
        for elem in space:
            self.assertEqual(elem, current)
            count += 1
            current += delta
        count_expected = 3 + 1
        self.assertEqual(count, count_expected)
        pass

    def test_elements_fatal_shift(self):
        start = datetime(2017, 1, 1, 6, 0)  # Shift A start
        end = datetime(2017, 1, 3, 0, 30)  # Shift C start day after, plus 2 hours and half
        delta = timedelta(hours=8)  # shift length
        space = xrange_datetime(start, end, delta)
        current = start
        count = 0
        for elem in space:
            self.assertEqual(elem, current)
            count += 1
            current += delta
        count_expected = 3 + 3
        self.assertEqual(count, count_expected)
        pass


if __name__ == '__main__':
    unittest.main()
