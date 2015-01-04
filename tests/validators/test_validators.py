# -*- coding: utf-8 -*-

from .. import CleoTestCase
from cleo.validators import (
    Validator, ValidationError,
    Boolean, Enum, Choice, Callable,
    Integer, Float, Range
)


class ValidatorTestCase(CleoTestCase):

    def test_is_valid(self):
        """
        Validator.is_valid() should return True if validate() passes False otherwise
        """
        validator = Validator()
        validator.validate = self.mock().MagicMock(return_value=True)

        self.assertTrue(validator.is_valid('foo'))

        validator.validate = self.mock().MagicMock(return_value=False)

        self.assertTrue(validator.is_valid('foo'))

    def test_error(self):
        validator = Validator()
        validator.name = 'foo'

        self.assertRaises(ValidationError, validator.error, 'foo')


class BooleanTestCase(CleoTestCase):

    def test_validate(self):
        validator = Boolean()

        self.assertTrue(validator.validate(True))
        self.assertFalse(validator.validate(False))

        self.assertTrue(validator.validate('1'))
        self.assertFalse(validator.validate('0'))

        self.assertTrue(validator.validate('true'))
        self.assertFalse(validator.validate('false'))

        self.assertTrue(validator.validate('yes'))
        self.assertFalse(validator.validate('no'))

        self.assertTrue(validator.validate('y'))
        self.assertFalse(validator.validate('n'))

        self.assertTrue(validator.validate('on'))
        self.assertFalse(validator.validate('off'))

        self.assertRaises(ValidationError, validator.validate, 'foo')


class EnumTestCase(CleoTestCase):

    def test_validate(self):
        validator = Enum(['foo', 'bar', 'baz'])

        self.assertEqual('foo', validator.validate('foo'))
        self.assertEqual('bar', validator.validate('bar'))
        self.assertEqual('baz', validator.validate('baz'))

        try:
            validator.validate('foooo')
            self.fail('ValidationError not raised')
        except ValidationError as e:
            self.assertRegex(
                str(e),
                'Invalid value \'foooo\' \(str\): must be one of \{%s}'
                % ', '.join(map(repr, set(['foo', 'bar', 'baz'])))
            )


class ChoiceTestCase(CleoTestCase):

    def test_validate(self):
        validator = Choice(['foo', 'bar', 'baz'])

        self.assertEqual('foo', validator.validate('foo'))
        self.assertEqual('bar', validator.validate('bar'))
        self.assertEqual('baz', validator.validate('baz'))

        try:
            validator.validate('foooo')
            self.fail('ValidationError not raised')
        except ValidationError as e:
            self.assertRegex(
                str(e),
                'Invalid value \'foooo\' \(str\): must be one of \{%s}'
                % ', '.join(map(repr, set(['foo', 'bar', 'baz'])))
            )


class CallableTestCase(CleoTestCase):

    def test_validate(self):
        validator = Callable(int)

        self.assertEqual(42, validator.validate(42))
        self.assertEqual(42, validator.validate('42'))

        self.assertRaises(
            ValidationError,
            validator.validate,
            'foo'
        )


class IntegerTestCase(CleoTestCase):

    def test_validate(self):
        validator = Integer()

        self.assertRaises(
            ValidationError,
            validator.validate,
            'foo'
        )

        self.assertRaises(
            ValidationError,
            validator.validate,
            '12.34'
        )

        self.assertEqual(57, validator.validate(57))
        self.assertEqual(57, validator.validate('57'))


class FloatTestCase(CleoTestCase):

    def test_validate(self):
        validator = Float()

        self.assertRaises(
            ValidationError,
            validator.validate,
            'foo'
        )

        self.assertEqual(57.0, validator.validate(57))
        self.assertEqual(57.0, validator.validate('57'))
        self.assertEqual(57.68, validator.validate(57.68))


class RangeTestCase(CleoTestCase):

    def test_validate_with_includes(self):
        validator = Range(12, 17)

        self.assertRaises(
            ValidationError,
            validator.validate,
            11
        )

        self.assertRaises(
            ValidationError,
            validator.validate,
            18
        )

        self.assertEqual(15, validator.validate(15))
        self.assertEqual(12, validator.validate(12))
        self.assertEqual(17, validator.validate(17))

    def test_validate_without_includes(self):
        validator = Range(12, 17, False, False)

        self.assertRaises(
            ValidationError,
            validator.validate,
            11
        )

        self.assertRaises(
            ValidationError,
            validator.validate,
            18
        )

        self.assertRaises(
            ValidationError,
            validator.validate,
            12
        )

        self.assertRaises(
            ValidationError,
            validator.validate,
            17
        )

        self.assertEqual(15, validator.validate(15))

    def test_validate_with_invalid_type(self):
        validator = Range(12, 17, validator=Integer())

        self.assertRaises(
            ValidationError,
            validator.validate,
            '12.57'
        )

        self.assertEqual(15, validator.validate(15))

    def test_validate_with_type(self):
        validator = Range(12, 17, validator=Float())

        self.assertEqual(15, validator.validate(15))
        self.assertEqual(12.57, validator.validate(12.57))
        self.assertEqual(12.57, validator.validate('12.57'))

    def test_validate_with_string(self):
        validator = Range('c', 'h', validator=None)

        self.assertRaises(
            ValidationError,
            validator.validate,
            'a'
        )

        self.assertRaises(
            ValidationError,
            validator.validate,
            'i'
        )

        self.assertEqual('d', validator.validate('d'))
        self.assertEqual('h', validator.validate('h'))
        self.assertEqual('c', validator.validate('c'))
