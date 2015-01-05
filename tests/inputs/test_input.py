# -*- coding: utf-8 -*-

import mock
from cleo.inputs import Input, InputDefinition, InputOption, InputArgument
from cleo.inputs.input import InvalidArgument, InvalidOption
from cleo.validators import Integer, Float

from .. import CleoTestCase


class MockInput(Input):

    def parse(self):
        self.arguments = {
            'arg': '57'
        }
        self.options = {
            'opt': '37.25'
        }

    def validate(self):
        pass


class MockWrongInput(Input):

    def parse(self):
        self.arguments = {
            'arg': 'foo'
        }
        self.options = {
            'opt': 'bar'
        }

    def validate(self):
        pass


class InputTest(CleoTestCase):

    def test_init(self):
        input = MockInput()

        self.assertIsNotNone(input.definition)
        self.assertEqual(input.arguments, {})
        self.assertEqual(input.arguments, {})

        definition = InputDefinition([
            InputArgument('arg'),
            InputOption('opt')
        ])

        input = MockInput(definition)

        self.assertEqual(definition, input.definition)
        self.assertEqual('57', input.arguments['arg'])
        self.assertEqual('37.25', input.options['opt'])

    def test_validate_arguments(self):
        definition = InputDefinition([
            InputArgument('arg', validator=Integer())
        ])

        input = MockInput(definition)

        input.validate_arguments()

        # Wrong type
        input = MockWrongInput(definition)

        self.assertRaises(
            InvalidArgument,
            input.validate_arguments
        )

    def test_validate_options(self):
        definition = InputDefinition([
            InputOption('opt', validator=Float())
        ])

        input = MockInput(definition)

        input.validate_options()

        # Wrong type
        input = MockWrongInput(definition)

        self.assertRaises(
            InvalidOption,
            input.validate_options
        )
