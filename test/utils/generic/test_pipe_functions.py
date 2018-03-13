import unittest

from giammis.utils.generic import pipe_functions


def foo(x):
    return x + 1


def boo(x):
    return x + 100


class PipeFunctionsTest(unittest.TestCase):
    def test_no_functions(self):
        zero = 0
        result = pipe_functions(functions=[], zero_value=zero)
        expected = zero
        self.assertEqual(result, expected)
        pass

    def test_single_function(self):
        zero = 0
        result = pipe_functions(functions=[foo], zero_value=zero)
        expected = zero + 1
        self.assertEqual(result, expected)
        result = pipe_functions(functions=[boo], zero_value=zero)
        expected = zero + 100
        self.assertEqual(result, expected)
        pass

    def test_two_functions(self):
        zero = 0
        result = pipe_functions(functions=[foo, foo], zero_value=zero)
        expected = zero + 1 + 1
        self.assertEqual(result, expected)
        result = pipe_functions(functions=[boo, boo], zero_value=zero)
        expected = zero + 100 + 100
        self.assertEqual(result, expected)
        result = pipe_functions(functions=[foo, boo], zero_value=zero)
        expected = zero + 1 + 100
        self.assertEqual(result, expected)
        result = pipe_functions(functions=[boo, foo], zero_value=zero)
        expected = zero + 1 + 100
        self.assertEqual(result, expected)
        pass

    def test_multiple_functions(self):
        zero = 0
        times = 10 ** 5
        functions = [foo] * times
        result = pipe_functions(functions, zero)
        expected = 1 * times
        self.assertEqual(result, expected)
        pass

    def test_two_ordered_functions(self):
        zero = 1
        add_one = lambda x: x + 1
        mul_ten = lambda x: x * 10
        result = pipe_functions([add_one, mul_ten], zero)
        expected = (zero + 1) * 10
        self.assertEqual(result, expected)
        result = pipe_functions([mul_ten, add_one], zero)
        expected = (zero * 10) + 1
        self.assertEqual(result, expected)
        pass

    def test_concat_string(self):
        zero = ''
        add_a = lambda s: s + 'a'
        result = pipe_functions(functions=[add_a, add_a, add_a], zero_value=zero)
        expected = 'aaa'
        self.assertEqual(result, expected)
        pass


if __name__ == '__main__':
    unittest.main()
