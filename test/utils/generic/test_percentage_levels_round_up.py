import unittest

from big_data_projects.plant.utils import percentage_levels_round_up

EPSILON = 0.00001
OPACITY_LEVELS = {
    3: [1.0, .50, .0],
    4: [1.0, .70, .30, .0],
    5: [1.0, .75, .50, .25, .0],
    6: [1.0, .80, .60, .40, .20, .0],
    7: [1.0, .85, .70, .50, .30, .15, .0],
    8: [1.0, .85, .70, .55, .40, .25, .10, .0],
}


class PercLevelsRoundUp(unittest.TestCase):
    def test_exact_levels_values(self):
        for n_levels, levels in OPACITY_LEVELS.items():
            for value in levels:
                result = percentage_levels_round_up(value, levels)
                expected = value
                self.assertEqual(result, expected, msg="{} and {}".format(result, expected))
        pass

    def test_big_numbers(self):
        big_numbers = [1.0, 2, 10, 200, 1000]
        for n_levels, levels in OPACITY_LEVELS.items():
            for value in big_numbers:
                result = percentage_levels_round_up(value, levels)
                expected = 1.0
                self.assertEqual(result, expected, msg="{} and {}".format(result, expected))
        pass

    def test_small_numbers(self):
        small_numbers = [0.0, -1, -2, -100, -1111]
        for n_levels, levels in OPACITY_LEVELS.items():
            for value in small_numbers:
                result = percentage_levels_round_up(value, levels)
                expected = 0.0
                self.assertEqual(result, expected, msg="{} and {}".format(result, expected))
        pass

    def test_just_above_thresholds_numbers(self):
        for n_levels, levels in OPACITY_LEVELS.items():
            for i in range(1, len(levels)):
                value = levels[i]
                value_moved = value + EPSILON
                result = percentage_levels_round_up(value_moved, levels)
                expected = levels[i - 1]
                self.assertEqual(result, expected, msg="{} and {}".format(result, expected))
        pass

    def test_just_below_thresholds_numbers(self):
        for n_levels, levels in OPACITY_LEVELS.items():
            for i in range(0, len(levels) - 1):
                value = levels[i]
                value_moved = value - EPSILON
                result = percentage_levels_round_up(value_moved, levels)
                expected = levels[i]
                self.assertEqual(result, expected, msg="{} and {}".format(result, expected))
        pass


if __name__ == '__main__':
    unittest.main()
