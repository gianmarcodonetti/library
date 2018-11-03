import unittest
from datetime import datetime, timedelta

from giammis.utils.gdatetime import round_datetime


class RoundDatetimeTest(unittest.TestCase):
    def test_already_rounded_day(self):
        for day in range(1, 28):
            date = datetime(2017, 4, day, 0, 0, 0)
            round_to = 60 * 60 * 24
            rounded = round_datetime(date, round_to)
            expected = date
            self.assertEqual(rounded, expected)
        pass

    def test_already_rounded_hour(self):
        for hour in range(0, 24):
            date = datetime(2017, 11, 17, hour, 0, 0)
            round_to = 60 * 60
            rounded = round_datetime(date, round_to)
            expected = date
            self.assertEqual(rounded, expected)
        pass

    def test_already_rounded_minute(self):
        for minute in range(0, 60):
            date = datetime(2017, 11, 17, 10, minute, 0)
            round_to = 60
            rounded = round_datetime(date, round_to)
            expected = date
            self.assertEqual(rounded, expected)
        pass

    def test_already_rounded_second(self):
        for second in range(0, 60):
            date = datetime(2017, 11, 17, 10, 23, second)
            round_to = 1
            rounded = round_datetime(date, round_to)
            expected = date
            self.assertEqual(rounded, expected)
        pass

    def test_already_rounded_hour_multiple(self):
        for hour in [0, 8, 16]:
            date = datetime(2017, 11, 17, hour, 0)
            round_to = 60 * 60 * 8
            rounded = round_datetime(date, round_to)
            expected = date
            self.assertEqual(rounded, expected)

        for hour in [0, 5, 10, 15, 20]:
            date = datetime(2017, 11, 17, hour, 0)
            round_to = 60 * 60 * 5
            rounded = round_datetime(date, round_to)
            expected = date
            self.assertEqual(rounded, expected)
        pass

    def test_next_hour(self):
        for hour in range(0, 24):
            date = datetime(2017, 11, 17, hour, 55, 0)
            round_to = 60 * 60
            rounded = round_datetime(date, round_to)
            expected = date + timedelta(hours=1) - timedelta(minutes=55)
            self.assertEqual(rounded, expected)
        pass

    def test_all_minutes_in_hour(self):
        for hour in range(0, 24):
            for minute in range(0, 60):
                date = datetime(2017, 11, 17, hour, minute, 0)
                round_to = 60 * 60
                rounded = round_datetime(date, round_to)
                if minute < 30:
                    expected = date - timedelta(minutes=minute)
                else:
                    expected = date + timedelta(minutes=60 - minute)
                self.assertEqual(rounded, expected)
        pass

    def test_all_hours_in_day(self):
        for day in range(1, 28):
            for hour in range(0, 24):
                date = datetime(2017, 11, day, hour, 0, 0)
                round_to = 60 * 60 * 24
                rounded = round_datetime(date, round_to)
                if hour < 12:
                    expected = date - timedelta(hours=hour)
                else:
                    expected = date + timedelta(hours=24 - hour)
                self.assertEqual(rounded, expected)
        pass


if __name__ == '__main__':
    unittest.main()
