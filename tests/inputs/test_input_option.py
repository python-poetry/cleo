# -*- coding: utf-8 -*-

from unittest import TestCase
from cleo.inputs.input_option import InputOption
from cleo.validators import Integer


class InputOptionTest(TestCase):

    def test_init(self):
        """
        InputOption.__init__() behaves properly
        """
        option = InputOption('foo')
        self.assertEqual('foo', option.get_name(), msg='__init__() takes a name as its first argument')
        option = InputOption('--foo')
        self.assertEqual('foo', option.get_name(), msg='__init__() removes the leading -- of the option name')

        # shortcut argument
        option = InputOption('foo', 'f')
        self.assertEqual('f', option.get_shortcut(), msg='__init__() can take a shortcut as its second argument')
        option = InputOption('foo', '-f')
        self.assertEqual('f', option.get_shortcut(), msg='__init__() removes the leading - of the shortcut')
        option = InputOption('foo')
        self.assertEqual(None, option.get_shortcut(), msg='__init__() makes the shortcut null by default')

        # mode argument
        option = InputOption('foo', 'f')
        self.assertFalse(option.accept_value(),
                         msg='__init__() gives a "InputOption.VALUE_NONE" mode by default')
        self.assertFalse(option.is_value_required(),
                         msg='__init__() gives a "InputOption.VALUE_NONE" mode by default')
        self.assertFalse(option.is_value_optional(),
                         msg='__init__() gives a "InputOption.VALUE_NONE" mode by default')

        option = InputOption('foo', 'f', None)
        self.assertFalse(option.accept_value(),
                         msg='__init__() can take "InputOption.VALUE_NONE" as its mode')
        self.assertFalse(option.is_value_required(),
                         msg='__init__() can take "InputOption.VALUE_NONE" as its mode')
        self.assertFalse(option.is_value_optional(),
                         msg='__init__() can take "InputOption.VALUE_NONE" as its mode')

        option = InputOption('foo', 'f', InputOption.VALUE_NONE)
        self.assertFalse(option.accept_value(),
                         msg='__init__() can take "InputOption.VALUE_NONE" as its mode')
        self.assertFalse(option.is_value_required(),
                         msg='__init__() can take "InputOption.VALUE_NONE" as its mode')
        self.assertFalse(option.is_value_optional(),
                         msg='__init__() can take "InputOption.VALUE_NONE" as its mode')

        option = InputOption('foo', 'f', InputOption.VALUE_REQUIRED)
        self.assertTrue(option.accept_value(),
                        msg='__init__() can take "InputOption.VALUE_REQUIRED" as its mode')
        self.assertTrue(option.is_value_required(),
                        msg='__init__() can take "InputOption.VALUE_REQUIRED" as its mode')
        self.assertFalse(option.is_value_optional(),
                         msg='__init__() can take "InputOption.VALUE_REQUIRED" as its mode')

        option = InputOption('foo', 'f', InputOption.VALUE_OPTIONAL)
        self.assertTrue(option.accept_value(),
                        msg='__init__() can take "InputOption.VALUE_OPTIONAL" as its mode')
        self.assertFalse(option.is_value_required(),
                         msg='__init__() can take "InputOption.VALUE_OPTIONAL" as its mode')
        self.assertTrue(option.is_value_optional(),
                        msg='__init__() can take "InputOption.VALUE_OPTIONAL" as its mode')

        self.assertRaises(Exception, InputOption, 'foo', 'f', 'ANOTHER_MODE')
        self.assertRaises(Exception, InputOption, 'foo', 'f', -1)

        validator = Integer()
        option = InputOption('foo', 'f', None, validator=validator)
        self.assertEqual(validator, option.get_validator())

        # Named validator
        validator = 'integer'
        option = InputOption('foo', 'f', None, validator=validator)
        self.assertIsInstance(option.get_validator(), Integer)

        # Native type
        validator = int
        option = InputOption('foo', 'f', None, validator=validator)
        self.assertIsInstance(option.get_validator(), Integer)

    def test_get_description(self):
        """
        InputOption.get_description() returns the message description
        """
        option = InputOption('foo', 'f', None, 'Some description')
        self.assertEqual('Some description', option.get_description(),
                         msg='.get_description() returns the message description')

    def test_get_default(self):
        """
        InputOption.get_default() returns the default value
        """
        option = InputOption('foo', 'f', InputOption.VALUE_OPTIONAL, '', 'default')
        self.assertEqual('default', option.get_default(),
                         msg='.get_default() returns the default value')
        option = InputOption('foo', 'f', InputOption.VALUE_REQUIRED, '', 'default')
        self.assertEqual('default', option.get_default(),
                         msg='.get_default() returns the default value')
        option = InputOption('foo', 'f', InputOption.VALUE_REQUIRED)
        self.assertEqual(None, option.get_default(),
                         msg='.get_default() returns None if no default value is configured')
        option = InputOption('foo', 'f', InputOption.VALUE_NONE)
        self.assertEqual(False, option.get_default(),
                         msg='.get_default() returns False if the option does not take a value')

    def test_set_default(self):
        """
        InputOption.set_default() sets the default value
        """
        option = InputOption('foo', 'f', InputOption.VALUE_REQUIRED, '', 'default')
        option.set_default(None)
        self.assertEqual(None, option.get_default(),
                         msg='.set_default() can reset the default value by passing None')
        option.set_default('another')
        self.assertEqual('another', option.get_default(),
                         msg='.set_default() changes the default value')

        option = InputOption('foo', 'f', InputOption.VALUE_NONE)
        self.assertRaises(Exception, option.set_default, 'default')
