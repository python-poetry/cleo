# -*- coding: utf-8 -*-

from cleo import argument, option, InputArgument, InputOption
from cleo.validators import Integer
from .. import CleoTestCase


class ApiTest(CleoTestCase):

    def test_argument(self):
        validator = Integer()
        arg = argument(
            'foo', 'The foo argument.',
            required=False, is_list=True,
            default=['default'], validator=validator
        )

        self.assertIsInstance(arg, InputArgument)
        self.assertEqual('foo', arg.get_name())
        self.assertEqual('The foo argument.', arg.get_description())
        self.assertEqual(['default'], arg.get_default())
        self.assertTrue(arg.is_list())
        self.assertFalse(arg.is_required())
        self.assertEqual(validator, arg.get_validator())

    def test_option(self):
        validator = Integer()
        opt = option(
            'foo', 'f', 'The foo option.',
            flag=True,
            validator=validator
        )

        self.assertIsInstance(opt, InputOption)
        self.assertEqual('foo', opt.get_name())
        self.assertEqual('The foo option.', opt.get_description())
        self.assertTrue(opt.is_flag())
        self.assertEqual(validator, opt.get_validator())

        opt = option(
            'foo', 'f', 'The foo option.',
            value_required=True,
            is_list=True,
            default=['default'],
            validator=validator
        )

        self.assertIsInstance(opt, InputOption)
        self.assertEqual('foo', opt.get_name())
        self.assertEqual('The foo option.', opt.get_description())
        self.assertFalse(opt.is_flag())
        self.assertTrue(opt.is_value_required())
        self.assertTrue(opt.is_list())
        self.assertEqual(validator, opt.get_validator())
