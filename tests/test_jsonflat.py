from unittest import TestCase

from jsonflat import JsonFlat


class JsonFlatTestCase(TestCase):

    def setUp(self):
        self.k = JsonFlat()
        self.input_rows = [
            {
                'a': 1,
                'b': 2,
                'c': {
                    'd': 5,
                    'f': {
                        'g': 90,
                        'h': 67,
                        'i': [1, 2, 3]
                    },
                    'j': [
                        {'k': 37, 'l': 67},
                        {'k': 22, 'l': 111}
                    ]
                },
                'e': 7,
                'i': [1, 2, 3, 4]
            },
            {
                'foo': 1,
                'bar': {},
                'c': 2,
                'd': [],
                'e': {'e1': []},
                'f': [[{}]],
                'g': [[[[]]]]
            },
            {},
            [{}],
            [[{}]]
        ]
        self.output_rows = {
            'field_names': ['a', 'b', 'c', 'c.d', 'c.f.g', 'c.f.h', 'c.f.i',
                            'c.j.k', 'c.j.l', 'e', 'e.e1', 'i', 'foo', 'bar',
                            'd', 'f', 'g'],
            'rows': [
                {'a': 1, 'b': 2, 'c.d': 5, 'c.f.g': 90, 'c.f.h': 67, 'e': 7,
                 'c.f.i': 1, 'c.j.k': 37, 'c.j.l': 67, 'i': 1},
                {'a': 1, 'b': 2, 'c.d': 5, 'c.f.g': 90, 'c.f.h': 67, 'e': 7,
                 'c.f.i': 2, 'c.j.k': 22, 'c.j.l': 111, 'i': 2},
                {'a': 1, 'b': 2, 'c.d': 5, 'c.f.g': 90, 'c.f.h': 67, 'e': 7,
                 'c.f.i': 3, 'i': 3},
                {'a': 1, 'b': 2, 'c.d': 5, 'c.f.g': 90, 'c.f.h': 67, 'e': 7,
                 'i': 4},
                {'foo': 1, 'bar': None, 'c': 2, 'd': None, 'e.e1': None,
                 'g': None, 'f': None},
                {},
                {},
                {}
            ]
        }

    def test_a_flat(self):
        # Empty list should return the same.
        fields, rows = self.k._a_flat([])
        self.assertEqual(len(fields), 0)
        self.assertListEqual(rows, [])
        # List in list. [[[[]]]] ==> [].
        fields, rows = self.k._a_flat([[[[]]]])
        self.assertEqual(len(fields), 0)
        self.assertListEqual(rows, [])
        # Dict in list. [{}] ==> [{}].
        fields, rows = self.k._a_flat([{}])
        self.assertEqual(len(fields), 0)
        self.assertListEqual(rows, [{}])
        # List of primitives as input.
        fields, rows = self.k._a_flat([1, 2, 'hello'])
        self.assertEqual(len(fields), 1)
        self.assertListEqual(rows, [{self.k._root_element_name: 1},
                                    {self.k._root_element_name: 2},
                                    {self.k._root_element_name: 'hello'}])

    def test_o_flat(self):
        # Empty dict should return the same.
        fields, row, lol = self.k._o_flat({})
        self.assertEqual(len(fields), 0)
        self.assertDictEqual(row, {})
        self.assertListEqual(lol, [])
        # Dict in dict. {'a': {}} ==> {'a': None}.
        fields, row, lol = self.k._o_flat({'a': {}})
        self.assertEqual(len(fields), 1)
        self.assertDictEqual(row, {'a': None})
        self.assertListEqual(lol, [])
        # List in dict. {'a': []} ==> {'a': None}.
        fields, row, lol = self.k._o_flat({'a': []})
        self.assertEqual(len(fields), 1)
        self.assertDictEqual(row, {'a': None})
        self.assertListEqual(lol, [])
        # Multiple lists in dict. {'a': [[[]]]} ==> {'a': None}.
        fields, row, lol = self.k._o_flat({'a': [[[]]]})
        self.assertEqual(len(fields), 1)
        self.assertDictEqual(row, {'a': None})
        self.assertListEqual(lol, [])
        # Multiple lists and a dict in dict.
        fields, row, lol = self.k._o_flat({'a': [[[{}]]]})
        self.assertEqual(len(fields), 1)
        self.assertDictEqual(row, {})
        self.assertListEqual(lol, [[{'a': None}]])

    def test_flatten(self):
        # Primitives as the arguments to flatten
        for primitive_arg in ['hello', 12, 2.3, True, None]:
            self.assertDictEqual(
                self.k.flatten(primitive_arg),
                {'field_names': [self.k._root_element_name],
                 'rows': [{self.k._root_element_name: primitive_arg}]})
        # Dict as the argument
        self.assertDictEqual(self.k.flatten({'a': {'b': 2}}),
                             {'field_names': ['a.b'], 'rows': [{'a.b': 2}]})
        # List as the argument
        self.assertDictEqual(self.k.flatten([]),
                             {'field_names': [], 'rows': []})
        self.assertDictEqual(self.k.flatten(self.input_rows),
                             self.output_rows)
