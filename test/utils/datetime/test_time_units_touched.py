import unittest
from datetime import datetime, timedelta

from giammis.utils.gdatetime import time_units_touched


class TimeUnitsTouchedTest(unittest.TestCase):
    def test_single_day(self):
        delta_seconds = 60 * 60 * 24  # 1 day
        duration = 60 * 60 * 3  # 3 hours
        # Completely inside
        for day in xrange(1, 28):
            date = datetime(2017, 4, day, 8, 30, 0)
            time_units = time_units_touched(date, duration_seconds=duration, delta_seconds=delta_seconds)
            expected = [datetime(2017, 4, day)]
            self.assertEqual(time_units, expected)
        pass

    def test_single_day_edges(self):
        delta_seconds = 60 * 60 * 24  # 1 day
        duration = 60 * 60 * 3  # 3 hours
        # Starting at the edge
        for day in xrange(1, 28):
            date = datetime(2017, 4, day, 0, 0, 0)
            time_units = time_units_touched(date, duration_seconds=duration, delta_seconds=delta_seconds)
            expected = [datetime(2017, 4, day)]
            self.assertEqual(time_units, expected)
        # Ending at the edge
        for day in xrange(1, 28):
            date = datetime(2017, 4, day, 21)
            time_units = time_units_touched(date, duration_seconds=duration, delta_seconds=delta_seconds)
            expected = [datetime(2017, 4, day)]
            self.assertEqual(time_units, expected)
        pass

    def test_single_hour(self):
        delta_seconds = 60 * 60  # 1 hour
        duration = 60 * 20  # 20 minutes
        # Completely inside
        for hour in xrange(0, 24):
            date = datetime(2017, 11, 17, hour, 20, 0)
            time_units = time_units_touched(date, duration_seconds=duration, delta_seconds=delta_seconds)
            expected = [datetime(2017, 11, 17, hour)]
            self.assertEqual(time_units, expected)
        pass

    def test_single_hour_edges(self):
        delta_seconds = 60 * 60  # 1 hour
        duration = 60 * 20  # 20 minutes
        # Starting at the edge
        for hour in xrange(0, 24):
            date = datetime(2017, 11, 17, hour, 0, 0)
            time_units = time_units_touched(date, duration_seconds=duration, delta_seconds=delta_seconds)
            expected = [datetime(2017, 11, 17, hour)]
            self.assertEqual(time_units, expected)
        # Ending at the edge
        for hour in xrange(0, 24):
            date = datetime(2017, 11, 17, hour, 40, 0)
            time_units = time_units_touched(date, duration_seconds=duration, delta_seconds=delta_seconds)
            expected = [datetime(2017, 11, 17, hour)]
            self.assertEqual(time_units, expected)
        pass

    def test_single_minute(self):
        delta_seconds = 60  # 1 minute
        duration = 20  # 20 seconds
        # Completely inside
        for minute in xrange(0, 60):
            date = datetime(2017, 11, 17, 10, minute, 20)
            time_units = time_units_touched(date, duration_seconds=duration, delta_seconds=delta_seconds)
            expected = [datetime(2017, 11, 17, 10, minute)]
            self.assertEqual(time_units, expected)
        pass

    def test_single_minute_edges(self):
        delta_seconds = 60  # 1 minute
        duration = 20  # 20 seconds
        # Starting at the edges
        for minute in xrange(0, 60):
            date = datetime(2017, 11, 17, 10, minute, 0)
            time_units = time_units_touched(date, duration_seconds=duration, delta_seconds=delta_seconds)
            expected = [datetime(2017, 11, 17, 10, minute)]
            self.assertEqual(time_units, expected)
        # Ending at the edges
        for minute in xrange(0, 60):
            date = datetime(2017, 11, 17, 10, minute, 40)
            time_units = time_units_touched(date, duration_seconds=duration, delta_seconds=delta_seconds)
            expected = [datetime(2017, 11, 17, 10, minute)]
            self.assertEqual(time_units, expected)
        pass

    def test_jumping_between_days(self):
        delta_seconds = 60 * 60 * 24  # 1 day
        date = datetime(2017, 5, 10, 8, 30)
        one_day = 60 * 60 * 24
        # 1 day
        time_units = time_units_touched(date, duration_seconds=one_day, delta_seconds=delta_seconds)
        expected = [datetime(2017, 5, 10), datetime(2017, 5, 11)]
        self.assertEqual(time_units, expected)
        # 2 days
        time_units = time_units_touched(date, duration_seconds=2 * one_day, delta_seconds=delta_seconds)
        expected = [datetime(2017, 5, 10), datetime(2017, 5, 11), datetime(2017, 5, 12)]
        self.assertEqual(time_units, expected)
        # 10 days
        time_units = time_units_touched(date, duration_seconds=10 * one_day, delta_seconds=delta_seconds)
        expected = [datetime(2017, 5, 10 + d) for d in range(11)]
        self.assertEqual(time_units, expected)
        pass

    def test_jumping_between_hours(self):
        delta_seconds = 60 * 60  # 1 hour
        date = datetime(2017, 5, 10, 8, 30)
        one_hour = 60 * 60
        # 1 hour
        time_units = time_units_touched(date, duration_seconds=one_hour, delta_seconds=delta_seconds)
        expected = [datetime(2017, 5, 10, 8), datetime(2017, 5, 10, 9)]
        self.assertEqual(time_units, expected)
        # 2 hours
        time_units = time_units_touched(date, duration_seconds=2 * one_hour, delta_seconds=delta_seconds)
        expected = [datetime(2017, 5, 10, 8), datetime(2017, 5, 10, 9), datetime(2017, 5, 10, 10)]
        self.assertEqual(time_units, expected)
        # 10 hours
        time_units = time_units_touched(date, duration_seconds=10 * one_hour, delta_seconds=delta_seconds)
        expected = [datetime(2017, 5, 10, 8 + h) for h in range(11)]
        self.assertEqual(time_units, expected)
        pass

    def test_jumping_between_hours_hard(self):
        delta_seconds = 60 * 60  # 1 hour
        date = datetime(2017, 5, 10, 8, 30)
        one_hour = 60 * 60
        # 24 hours
        time_units = time_units_touched(date, duration_seconds=24 * one_hour, delta_seconds=delta_seconds)
        expected = [datetime(2017, 5, 10, 8) + timedelta(seconds=60 * 60 * h) for h in range(25)]
        self.assertEqual(time_units, expected)
        # 72 hours
        time_units = time_units_touched(date, duration_seconds=72 * one_hour, delta_seconds=delta_seconds)
        expected = [datetime(2017, 5, 10, 8) + timedelta(seconds=60 * 60 * h) for h in range(73)]
        self.assertEqual(time_units, expected)
        pass


if __name__ == '__main__':
    unittest.main()
