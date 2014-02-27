# -*- coding: utf-8 -*-

from cleo.input import ListInput, InputDefinition, InputArgument, InputOption

from .. import CleoTestCase


class ListInputTest(CleoTestCase):

    def test_get_first_argument(self):
        input_ = ListInput([])
        self.assertEqual(None, input_.get_first_argument())
        input_ = ListInput([('name', 'John')])
        self.assertEqual('John', input_.get_first_argument())
        input_ = ListInput([('--foo', 'bar'), ('name', 'John')])
        self.assertEqual('John', input_.get_first_argument())

    def test_has_parameter_option(self):
        input_ = ListInput([('name', 'John'), ('--foo', 'bar')])

        self.assertTrue(input_.has_parameter_option('--foo'))
        self.assertFalse(input_.has_parameter_option('--bar'))

        input_ = ListInput(['--foo'])
        self.assertTrue(input_.has_parameter_option('--foo'))

    def test_parse_arguments(self):
        input_ = ListInput(
            [('name', 'foo')],
            InputDefinition([
                InputArgument('name')
            ])
        )

        self.assertEqual({'name': 'foo'}, input_.get_arguments())

    def test_parse_options(self):
        for iopts, opts, expected in self.provide_options():
            input_ = ListInput(iopts, InputDefinition(opts))

            self.assertEqual(expected, input_.get_options())

    def provide_options(self):
        return [
            (
                [('--foo', 'bar')],
                [InputOption('foo')],
                {'foo': 'bar'}
            ),
            (
                [('--foo', 'bar')],
                [InputOption('foo', 'f', InputOption.VALUE_OPTIONAL, '', 'default')],
                {'foo': 'bar'}
            ),
            (
                ['--foo'],
                [InputOption('foo', 'f', InputOption.VALUE_OPTIONAL, '', 'default')],
                {'foo': 'default'}
            ),
            (
                [('-f', 'bar')],
                [InputOption('foo', 'f')],
                {'foo': 'bar'}
            ),
        ]

    def test_parse_invalid_input(self):
        for args, definition, expected in self.provider_invalid_input():
            self.assertRaisesRegexp(
                Exception,
                expected,
                ListInput,
                args,
                definition
            )

    def provider_invalid_input(self):
        return [
            (
                [('foo', 'bar')],
                InputDefinition([
                    InputArgument('name')
                ]),
                'The "foo" argument does not exist.'
            ),
            (
                ['--foo'],
                InputDefinition([
                    InputOption('foo', 'f', InputOption.VALUE_REQUIRED)
                ]),
                'The "--foo" option requires a value.'
            ),
            (
                [('--foo', 'foo')],
                InputDefinition(),
                'The "--foo" option does not exist.'
            ),
            (
                [('-f', 'foo')],
                InputDefinition(),
                'The "-f" option does not exist.'
            ),
        ]
