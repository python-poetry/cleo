# -*- coding: utf-8 -*-

from cleo.parser import Parser
from cleo.validators import Integer, Boolean
from . import CleoTestCase


class ParserTestCase(CleoTestCase):

    def test_basic_parameter_parsing(self):
        results = Parser.parse('command:name')

        self.assertEqual('command:name', results['name'])

        results = Parser.parse('command:name {argument} {--option}')

        self.assertEqual('command:name', results['name'])
        self.assertEqual('argument', results['arguments'][0].get_name())
        self.assertEqual('option', results['options'][0].get_name())
        self.assertFalse(results['options'][0].accept_value())

        results = Parser.parse('command:name {argument*} {--option=}')

        self.assertEqual('command:name', results['name'])
        self.assertEqual('argument', results['arguments'][0].get_name())
        self.assertTrue(results['arguments'][0].is_list())
        self.assertTrue(results['arguments'][0].is_required())
        self.assertEqual('option', results['options'][0].get_name())
        self.assertTrue(results['options'][0].accept_value())

        results = Parser.parse('command:name {argument?*} {--option=*}')

        self.assertEqual('command:name', results['name'])
        self.assertEqual('argument', results['arguments'][0].get_name())
        self.assertTrue(results['arguments'][0].is_list())
        self.assertFalse(results['arguments'][0].is_required())
        self.assertEqual('option', results['options'][0].get_name())
        self.assertTrue(results['options'][0].accept_value())
        self.assertTrue(results['options'][0].is_list())

        results = Parser.parse('command:name {argument?* : The argument description.}    {--option=* : The option description.}')

        self.assertEqual('command:name', results['name'])
        self.assertEqual('argument', results['arguments'][0].get_name())
        self.assertEqual('The argument description.', results['arguments'][0].get_description())
        self.assertTrue(results['arguments'][0].is_list())
        self.assertFalse(results['arguments'][0].is_required())
        self.assertEqual('option', results['options'][0].get_name())
        self.assertEqual('The option description.', results['options'][0].get_description())
        self.assertTrue(results['options'][0].accept_value())
        self.assertTrue(results['options'][0].is_list())

        results = Parser.parse(
            'command:name '
            '{argument?* : The argument description.}    '
            '{--option=* : The option description.}'
        )

        self.assertEqual('command:name', results['name'])
        self.assertEqual('argument', results['arguments'][0].get_name())
        self.assertEqual('The argument description.', results['arguments'][0].get_description())
        self.assertTrue(results['arguments'][0].is_list())
        self.assertFalse(results['arguments'][0].is_required())
        self.assertEqual('option', results['options'][0].get_name())
        self.assertEqual('The option description.', results['options'][0].get_description())
        self.assertTrue(results['options'][0].accept_value())
        self.assertTrue(results['options'][0].is_list())

    def test_shortcut_name_parsing(self):
        results = Parser.parse('command:name {--o|option}')

        self.assertEqual('command:name', results['name'])
        self.assertEqual('option', results['options'][0].get_name())
        self.assertEqual('o', results['options'][0].get_shortcut())
        self.assertFalse(results['options'][0].accept_value())

        results = Parser.parse('command:name {--o|option=}')

        self.assertEqual('command:name', results['name'])
        self.assertEqual('option', results['options'][0].get_name())
        self.assertEqual('o', results['options'][0].get_shortcut())
        self.assertTrue(results['options'][0].accept_value())

        results = Parser.parse('command:name {--o|option=*}')

        self.assertEqual('command:name', results['name'])
        self.assertEqual('option', results['options'][0].get_name())
        self.assertEqual('o', results['options'][0].get_shortcut())
        self.assertTrue(results['options'][0].accept_value())
        self.assertTrue(results['options'][0].is_list())

        results = Parser.parse('command:name {--o|option=* : The option description.}')

        self.assertEqual('command:name', results['name'])
        self.assertEqual('option', results['options'][0].get_name())
        self.assertEqual('o', results['options'][0].get_shortcut())
        self.assertEqual('The option description.', results['options'][0].get_description())
        self.assertTrue(results['options'][0].accept_value())
        self.assertTrue(results['options'][0].is_list())

        results = Parser.parse(
            'command:name '
            '{--o|option=* : The option description.}'
        )

        self.assertEqual('command:name', results['name'])
        self.assertEqual('option', results['options'][0].get_name())
        self.assertEqual('o', results['options'][0].get_shortcut())
        self.assertEqual('The option description.', results['options'][0].get_description())
        self.assertTrue(results['options'][0].accept_value())
        self.assertTrue(results['options'][0].is_list())

    def test_validator_parsing(self):
        results = Parser.parse('command:name {argument (integer)} {--option (boolean) : Description with (parenthesis)}')

        self.assertEqual('argument', results['arguments'][0].get_name())
        self.assertEqual('option', results['options'][0].get_name())
        self.assertIsInstance(results['arguments'][0].get_validator(), Integer)
        self.assertIsInstance(results['options'][0].get_validator(), Boolean)
