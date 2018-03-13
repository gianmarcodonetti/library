import unittest

from giammis.utils.generic import merge_dictionaries


class MergeDictionariesTest(unittest.TestCase):
    def test_empty(self):
        result = merge_dictionaries([])
        expected = {}
        self.assertEqual(result, expected)
        pass

    def test_single_dict(self):
        diz = {'a': 100}
        result = merge_dictionaries([diz])
        expected = diz
        self.assertEqual(result, expected)
        pass

    def test_disjoint_dict(self):
        diz = {'a': 1, 'b': 1, 'c': 1, 'd': 1}
        dik = {'z': 2, 'x': 2, 'w': 2, 'y': 2}
        result = merge_dictionaries([diz, dik])
        expected = {'a': 1, 'b': 1, 'c': 1, 'd': 1, 'z': 2, 'x': 2, 'w': 2, 'y': 2}
        self.assertEqual(result, expected)

        result = merge_dictionaries([dik, diz])
        self.assertEqual(result, expected)
        pass

    def test_joint_dict(self):
        diz = {'a': 1, 'b': 1, 'c': 1, 'd': 1, 'joint': False}
        dik = {'z': 2, 'x': 2, 'w': 2, 'y': 2, 'joint': True}
        result = merge_dictionaries([diz, dik])
        expected = {'a': 1, 'b': 1, 'c': 1, 'd': 1, 'z': 2, 'x': 2, 'w': 2, 'y': 2, 'joint': True}
        self.assertEqual(result, expected)
        result = merge_dictionaries([dik, diz])
        expected = {'a': 1, 'b': 1, 'c': 1, 'd': 1, 'z': 2, 'x': 2, 'w': 2, 'y': 2, 'joint': False}
        self.assertEqual(result, expected)
        pass

    def test_three_join_dict(self):
        diz = {'a': 1, 'b': 1, 'c': 1, 'd': 1, 'joint': 'first'}
        dik = {'z': 2, 'x': 2, 'w': 2, 'y': 2, 'joint': 'second'}
        diw = {'m': 3, 'n': 3, 'l': 3, 'p': 3, 'joint': 'third'}
        result = merge_dictionaries([diz, dik, diw])  # 1st, 2nd, 3rd
        expected = {'a': 1, 'b': 1, 'c': 1, 'd': 1, 'z': 2, 'x': 2, 'w': 2, 'y': 2, 'm': 3, 'n': 3, 'l': 3, 'p': 3,
                    'joint': 'third'}
        self.assertEqual(result, expected)
        result = merge_dictionaries([dik, diw, diz])  # 2nd, 3rd, 1st
        expected = {'a': 1, 'b': 1, 'c': 1, 'd': 1, 'z': 2, 'x': 2, 'w': 2, 'y': 2, 'm': 3, 'n': 3, 'l': 3, 'p': 3,
                    'joint': 'first'}
        self.assertEqual(result, expected)
        result = merge_dictionaries([diw, diz, dik])  # 3rd, 1st, 2nd
        expected = {'a': 1, 'b': 1, 'c': 1, 'd': 1, 'z': 2, 'x': 2, 'w': 2, 'y': 2, 'm': 3, 'n': 3, 'l': 3, 'p': 3,
                    'joint': 'second'}
        self.assertEqual(result, expected)
        pass

    def test_no_keys_inside(self):
        diz = {'a': 1, 'b': 1, 'c': 1, 'd': 1, 'joint': False}
        dik = {'z': 2, 'x': 2, 'w': 2, 'y': 2, 'joint': True}
        result = merge_dictionaries([diz, dik], keys_to_remove=['aaa', 'bbb', 'zxwy'])
        expected = {'a': 1, 'b': 1, 'c': 1, 'd': 1, 'z': 2, 'x': 2, 'w': 2, 'y': 2, 'joint': True}
        self.assertEqual(result, expected)
        pass

    def test_some_keys_inside(self):
        diz = {'a': 1, 'b': 1, 'c': 1, 'd': 1, 'joint': False}
        dik = {'z': 2, 'x': 2, 'w': 2, 'y': 2, 'joint': True}
        result = merge_dictionaries([diz, dik], keys_to_remove=['aaa', 'bbb', 'z', 'x', 'w'])
        expected = {'a': 1, 'b': 1, 'c': 1, 'd': 1, 'y': 2, 'joint': True}
        self.assertEqual(result, expected)
        pass

    def test_all_keys_inside(self):
        diz = {'a': 1, 'b': 1, 'c': 1, 'd': 1, 'joint': False}
        dik = {'z': 2, 'x': 2, 'w': 2, 'y': 2, 'joint': True}
        result = merge_dictionaries([diz, dik], keys_to_remove=['z', 'x', 'w'])
        expected = {'a': 1, 'b': 1, 'c': 1, 'd': 1, 'y': 2, 'joint': True}
        self.assertEqual(result, expected)
        pass

    def test_all_keys_removes(self):
        diz = {'a': 1, 'b': 1, 'c': 1, 'd': 1, 'joint': False}
        dik = {'z': 2, 'x': 2, 'w': 2, 'y': 2, 'joint': True}
        result = merge_dictionaries([diz, dik], keys_to_remove=['a', 'b', 'c', 'd', 'z', 'x', 'w', 'y', 'joint'])
        expected = {}
        self.assertEqual(result, expected)
        pass

    def test_remove_joint_key(self):
        diz = {'a': 1, 'b': 1, 'c': 1, 'd': 1, 'joint': 'first'}
        dik = {'z': 2, 'x': 2, 'w': 2, 'y': 2, 'joint': 'second'}
        diw = {'m': 3, 'n': 3, 'l': 3, 'p': 3, 'joint': 'third'}
        result = merge_dictionaries([diz, dik, diw], keys_to_remove=['joint'])  # 1st, 2nd, 3rd
        expected = {'a': 1, 'b': 1, 'c': 1, 'd': 1, 'z': 2, 'x': 2, 'w': 2, 'y': 2, 'm': 3, 'n': 3, 'l': 3, 'p': 3}
        self.assertEqual(result, expected)
        pass


if __name__ == '__main__':
    unittest.main()
