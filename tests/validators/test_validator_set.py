# -*- coding: utf-8 -*-

from .. import CleoTestCase
from cleo.validators import ValidatorSet, Boolean, Enum, Integer, Float, Range


class ValidatorSetTestCase(CleoTestCase):

    def test_init(self):
        validator_set = ValidatorSet()

        self.assertEqual({}, validator_set.validators)

        validator_set = ValidatorSet([Boolean])

        self.assertEqual(Boolean, validator_set.validators['boolean'])

    def test_register(self):
        validator_set = ValidatorSet()

        validator_set.register(Boolean)
        self.assertEqual(1, len(validator_set.validators))
        self.assertEqual(Boolean, validator_set.validators['boolean'])

        validator_set.register(Enum)
        self.assertEqual(3, len(validator_set.validators))
        self.assertEqual(Enum, validator_set.validators['enum'])
        self.assertEqual(Enum, validator_set.validators['choice'])

    def test_register_with_non_validator(self):
        validator_set = ValidatorSet()

        self.assertRaises(
            Exception,
            validator_set.register,
            'foo'
        )

        class Foo(object):

            name = 'foo'

        self.assertRaises(
            Exception,
            validator_set.register,
            Foo
        )

    def test_get(self):
        validator_set = ValidatorSet([
            Boolean,
            Enum
        ])

        self.assertIsInstance(validator_set.get('boolean'), Boolean)
        self.assertIsInstance(validator_set.get(Boolean()), Boolean)
        self.assertIsNone(validator_set.get('string'))

        try:
            validator_set.get('foo')
            self.fail('ValidatorSet.get() with unknown validator should fail')
        except Exception as e:
            self.assertRegex(
                str(e),
                'Unable to find a validator with name "foo"'
            )

    def test_get_native_types(self):
        validator_set = ValidatorSet()

        self.assertIsInstance(validator_set.get(bool), Boolean)
        self.assertIsInstance(validator_set.get(int), Integer)
        self.assertIsInstance(validator_set.get(float), Float)
        self.assertIsNone(validator_set.get(str))
