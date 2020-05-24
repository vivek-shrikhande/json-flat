import unittest

from jsonflat import Field


class FieldTestCase(unittest.TestCase):

    def setUp(self):
        self.field = Field(False)

    def test_set_field(self):
        field_a = self.field.set_field('a')
        # check if newly created Field has __self set to True
        self.assertEqual(getattr(field_a, '_Field__self'), True)
        # check if newly created Field does not have __data attribute
        self.assertRaises(AttributeError, getattr, field_a, '_Field__data')
        # add a Field group to field_a and check if it's __data is set
        fg_a1 = field_a.set_field_group('a1')
        self.assertDictEqual(getattr(field_a, '_Field__data'), {'a1': fg_a1})

    def test_set_field_group(self):
        fg_b = self.field.set_field_group('b')
        # check if newly created Field group has __self set to False
        self.assertEqual(getattr(fg_b, '_Field__self'), False)
        # check if newly created Field does not have __data attribute
        self.assertRaises(AttributeError, getattr, fg_b, '_Field__data')
        # add a new Field to fg_b and check if fg_b has __data attribute
        fg_b1 = fg_b.set_field('b1')
        self.assertDictEqual(getattr(fg_b, '_Field__data'), {'b1': fg_b1})
        # add a Field with the same name i.e. 'b' and check if it's
        # __self is set to True
        self.field.set_field('b')
        self.assertEqual(getattr(fg_b, '_Field__self'), True)

    def test_normalization(self):
        # empty Field group
        fg_c = self.field.set_field_group('c')
        fg_c.set_field_group('c1')
        self.assertListEqual(fg_c.get_normalized_fields(), [])
        # with Field
        fg_c.set_field_group('c1').set_field('c13')
        self.assertListEqual(fg_c.get_normalized_fields(), ['c1.c13'])
        # with Field group
        # normalization does not sort; instead preserves order of insertion
        fg_c.set_field_group('c1').set_field('c12')
        self.assertListEqual(fg_c.get_normalized_fields(),
                             ['c1.c13', 'c1.c12'])
        # with Field and Field group
        fg_c.set_field('c1')
        self.assertListEqual(fg_c.get_normalized_fields(),
                             ['c1', 'c1.c13', 'c1.c12'])

    def test_repr(self):
        field_d = self.field.set_field('d')
        # Field without __data
        self.assertEqual(field_d.__repr__(), "{'__SELF__': true}")
        # Field with __data
        field_d1 = field_d.set_field('d1')
        self.assertEqual(field_d.__repr__(),
                         "{'__SELF__': true, 'd1': {'__SELF__': true}}")
        # Field group with empty __data
        fg_e = self.field.set_field_group('e')
        self.assertEqual(fg_e.__repr__(), "{}")
        # Field group with __data
        fg_e.set_field_group('e1')
        self.assertEqual(fg_e.__repr__(), "{'e1': {}}")

    def test_str(self):
        field_f = self.field.set_field('f')
        # Field without __data
        self.assertEqual(field_f.__str__(), 'true')
        # Field with __data
        field_f1 = field_f.set_field('f1')
        self.assertEqual(field_f.__str__(), '{"__SELF__": true, "f1": true}')
        # Field group with empty __data
        fg_g = self.field.set_field_group('g')
        self.assertEqual(fg_g.__str__(), "{}")
        # Field group with __data
        fg_g.set_field_group('g1')
        self.assertEqual(fg_g.__str__(), '{"g1": {}}')

    def test_len(self):
        # with __self set to True, without __data
        field_g = self.field.set_field('g')
        self.assertEqual(len(field_g), 1)
        # with __self set to True, with __data
        field_g.set_field('g1')
        self.assertEqual(len(field_g), 2)
        # with __self set to False, without __data
        fg_h = self.field.set_field_group('h')
        self.assertEqual(len(fg_h), 0)
        # with __self set to False, with __data
        fg_h.set_field('h1')
        self.assertEqual(len(fg_h), 1)


if __name__ == '__main__':
    unittest.main()
