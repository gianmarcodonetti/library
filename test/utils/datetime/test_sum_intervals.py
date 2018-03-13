import unittest
from datetime import datetime, timedelta

from big_data_projects.plant.utils import sum_intervals


class SumIntervalsTest(unittest.TestCase):
    def test_single_interval_simple(self):
        start_date = datetime(2017, 10, 1, 10)
        duration = 60 * 60 * 2
        end_date = start_date + timedelta(seconds=duration)
        result = sum_intervals([(start_date, end_date)])
        expected = duration
        self.assertEqual(result, expected)
        pass

    def test_single_interval_hard(self):
        start_date = datetime(2017, 10, 1, 18, 10)
        duration = 60 * 60 * 24 + 60 * 60 * 2 + 60 * 45
        end_date = start_date + timedelta(seconds=duration)
        result = sum_intervals([(start_date, end_date)])
        expected = duration
        self.assertEqual(result, expected)
        pass

    def test_two_not_overlapping(self):
        start_date_1 = datetime(1992, 1, 1, 1)
        duration_1 = 60 * 60 * 3
        end_date_1 = start_date_1 + timedelta(seconds=duration_1)
        start_date_2 = datetime(2017, 1, 1, 1)
        duration_2 = 60 * 60 * 5
        end_date_2 = start_date_2 + timedelta(seconds=duration_2)
        result = sum_intervals([(start_date_1, end_date_1), (start_date_2, end_date_2)])
        expected = duration_1 + duration_2
        self.assertEqual(result, expected)
        pass

    def test_inside_intervals(self):
        start_date_1 = datetime(1992, 1, 1, 1)
        duration_1 = 60 * 60 * 3
        end_date_1 = start_date_1 + timedelta(seconds=duration_1)
        start_date_2 = start_date_1
        duration_2 = 60 * 60 * 1
        end_date_2 = start_date_2 + timedelta(seconds=duration_2)
        result = sum_intervals([(start_date_1, end_date_1), (start_date_2, end_date_2)])
        expected = duration_1
        self.assertEqual(result, expected)
        pass

    def test_overlapping_intervals_simple(self):
        start_date_1 = datetime(1992, 1, 1, 1)
        duration_1 = 60 * 60 * 2
        end_date_1 = start_date_1 + timedelta(seconds=duration_1)
        start_date_2 = datetime(1992, 1, 1, 2)
        duration_2 = 60 * 60 * 2
        end_date_2 = start_date_2 + timedelta(seconds=duration_2)
        result = sum_intervals([(start_date_1, end_date_1), (start_date_2, end_date_2)])
        expected = 60 * 60 * 3
        self.assertEqual(result, expected)
        pass

    def test_overlapping_intervals_hard(self):
        start_date_1 = datetime(1992, 1, 1, 0)
        duration_1 = 60 * 60 * 10
        end_date_1 = start_date_1 + timedelta(seconds=duration_1)
        start_date_2 = datetime(1992, 1, 1, 14)
        duration_2 = 60 * 60 * 10
        end_date_2 = start_date_2 + timedelta(seconds=duration_2)
        start_date_3 = datetime(1992, 1, 1, 10)
        duration_3 = 60 * 60 * 8
        end_date_3 = start_date_3 + timedelta(seconds=duration_3)
        start_date_4 = datetime(1992, 1, 1, 6)
        duration_4 = 60 * 45
        end_date_4 = start_date_4 + timedelta(seconds=duration_4)
        result = sum_intervals([(start_date_1, end_date_1), (start_date_2, end_date_2), (start_date_3, end_date_3),
                                (start_date_4, end_date_4)])
        expected = 60 * 60 * 24
        self.assertEqual(result, expected)
        pass


if __name__ == '__main__':
    unittest.main()
