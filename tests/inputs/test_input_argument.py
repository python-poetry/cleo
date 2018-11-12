# -*- coding: utf-8 -*-

from unittest import TestCase
from cleo.inputs.input_argument import InputArgument
from cleo.validators import Integer


class InputArgumentTest(TestCase):
    def test_init(self):
        """
        InputArgument.__init__() behaves properly
        """
        argument = InputArgument("foo")
        self.assertEqual(
            "foo",
            argument.get_name(),
            msg="__init__() takes a name as its first argument",
        )

        # mode argument
        argument = InputArgument("foo")
        self.assertFalse(
            argument.is_required(),
            msg='__init__() gives a "InputArgument.OPTIONAL" mode by default',
        )

        argument = InputArgument("foo", None)
        self.assertFalse(
            argument.is_required(),
            msg='__init__() can take "InputArgument.OPTIONAL" as its mode',
        )

        argument = InputArgument("foo", InputArgument.OPTIONAL)
        self.assertFalse(
            argument.is_required(),
            msg='__init__() can take "InputArgument.OPTIONAL" as its mode',
        )

        argument = InputArgument("foo", InputArgument.REQUIRED)
        self.assertTrue(
            argument.is_required(),
            msg='__init__() can take "InputArgument.REQUIRED" as its mode',
        )

        self.assertRaises(Exception, InputArgument, "foo", "ANOTHER_MODE")
        self.assertRaises(Exception, InputArgument, "foo", -1)

        validator = Integer()
        argument = InputArgument("foo", None, validator=validator)
        self.assertEqual(validator, argument.get_validator())

        # Named validator
        validator = "integer"
        argument = InputArgument("foo", None, validator=validator)
        self.assertIsInstance(argument.get_validator(), Integer)

        # Native type
        validator = int
        argument = InputArgument("foo", None, validator=validator)
        self.assertIsInstance(argument.get_validator(), Integer)

    def test_is_list(self):
        """
        InputArgument.is_list() returns true if the argument can be an array'
        """
        argument = InputArgument("foo", InputArgument.IS_LIST)
        self.assertTrue(argument.is_list())

        argument = InputArgument("foo", InputArgument.OPTIONAL | InputArgument.IS_LIST)
        self.assertTrue(argument.is_list())

        argument = InputArgument("foo", InputArgument.OPTIONAL)
        self.assertFalse(argument.is_list())

    def test_get_description(self):
        """
        InputArgument.get_description() returns the message description
        """
        argument = InputArgument("foo", None, "Some description")
        self.assertEqual(
            "Some description",
            argument.get_description(),
            msg=".get_description() returns the message description",
        )

    def test_get_default(self):
        """
        InputArgument.get_default() returns the default value
        """
        argument = InputArgument("foo", InputArgument.OPTIONAL, "", "default")
        self.assertEqual(
            "default",
            argument.get_default(),
            msg=".get_default() returns the default value",
        )

    def test_set_default(self):
        """
        InputArgument.set_default() sets the default value
        """
        argument = InputArgument("foo", InputArgument.OPTIONAL, "", "default")
        argument.set_default(None)
        self.assertEqual(
            None,
            argument.get_default(),
            msg=".set_default() can reset the default value by passing None",
        )
        argument.set_default("another")
        self.assertEqual(
            "another",
            argument.get_default(),
            msg=".set_default() changes the default value",
        )

        argument = InputArgument("foo", InputArgument.REQUIRED)
        self.assertRaises(Exception, argument.set_default, "default")
