import unittest
from datetime import datetime, timedelta

from big_data_projects.plant.utils import floor_datetime


class FloorDatetimeTest(unittest.TestCase):
    def test_already_floored_day(self):
        for day in xrange(1, 28):
            date = datetime(2017, 4, day, 0, 0, 0)
            round_to = 60 * 60 * 24
            rounded = floor_datetime(date, round_to)
            expected = date
            self.assertEqual(rounded, expected)
        pass

    def test_already_floored_hour(self):
        for hour in xrange(0, 24):
            date = datetime(2017, 11, 17, hour, 0, 0)
            round_to = 60 * 60
            rounded = floor_datetime(date, round_to)
            expected = date
            self.assertEqual(rounded, expected)
        pass

    def test_already_floored_minute(self):
        for minute in xrange(0, 60):
            date = datetime(2017, 11, 17, 10, minute, 0)
            round_to = 60
            rounded = floor_datetime(date, round_to)
            expected = date
            self.assertEqual(rounded, expected)
        pass

    def test_already_floored_second(self):
        for second in xrange(0, 60):
            date = datetime(2017, 11, 17, 10, 23, second)
            round_to = 1
            rounded = floor_datetime(date, round_to)
            expected = date
            self.assertEqual(rounded, expected)
        pass

    def test_already_floored_hour_multiple(self):
        for hour in [0, 8, 16]:
            date = datetime(2017, 11, 17, hour, 0)
            round_to = 60 * 60 * 8
            rounded = floor_datetime(date, round_to)
            expected = date
            self.assertEqual(rounded, expected)

        for hour in [0, 5, 10, 15, 20]:
            date = datetime(2017, 11, 17, hour, 0)
            round_to = 60 * 60 * 5
            rounded = floor_datetime(date, round_to)
            expected = date
            self.assertEqual(rounded, expected)
        pass

    def test_next_hour(self):
        for hour in xrange(0, 1):
            date = datetime(2017, 11, 17, hour, 55, 0)
            round_to = 60 * 60
            rounded = floor_datetime(date, round_to)
            expected = date - timedelta(minutes=55)
            self.assertEqual(rounded, expected)
        pass

        def test_all_minutes_in_hour(self):
            for hour in xrange(0, 24):
                for minute in xrange(1, 60):
                    date = datetime(2017, 11, 17, hour, minute, 0)
                    round_to = 60 * 60
                    rounded = floor_datetime(date, round_to)
                    expected = date - timedelta(minutes=minute)  # always current hour
                    self.assertEqual(rounded, expected)
            pass

        def test_all_hours_in_day(self):
            for day in xrange(1, 28):
                for hour in xrange(1, 24):
                    date = datetime(2017, 11, day, hour, 0, 0)
                    round_to = 60 * 60 * 24
                    rounded = floor_datetime(date, round_to)
                    expected = date - timedelta(hours=hour)  # always current day
                    self.assertEqual(rounded, expected)
            pass


if __name__ == '__main__':
    unittest.main()
