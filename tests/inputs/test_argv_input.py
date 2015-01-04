# -*- coding: utf-8 -*-

import sys
from cleo.inputs import ArgvInput, InputDefinition, InputOption, InputArgument

from .. import CleoTestCase


class ArgvInputTest(CleoTestCase):

    def test_init(self):
        sys.argv = ['cli.py', 'foo']
        input_ = ArgvInput()

        self.assertEqual(
            ['foo'],
            input_._ArgvInput__tokens
        )
        self.assertEqual(
            ['cli.py', 'foo'],
            sys.argv
        )

    def test_parse_arguments(self):
        input_ = ArgvInput(['cli.py', 'foo'])
        input_.bind(
            InputDefinition([
                InputArgument('name')
            ])
        )

        self.assertEqual({'name': 'foo'}, input_.get_arguments())

        # parse is stateless
        self.assertEqual({'name': 'foo'}, input_.get_arguments())

    def test_parse_options(self):
        for argv, options, expected_options, message in self.provide_options():
            input_ = ArgvInput(argv)
            input_.bind(InputDefinition(options))

            self.assertEqual(
                expected_options,
                input_.get_options(),
                msg=message
            )

    def provide_options(self):
        return [
            (
                ['cli.py', '--foo'],
                [InputOption('foo')],
                {'foo': True},
                '.parse() parses long options without a value'
            ),
            (
                ['cli.py', '--foo=bar'],
                [InputOption('foo', 'f', InputOption.VALUE_REQUIRED)],
                {'foo': 'bar'},
                '.parse() parses long options with a required value (with a = separator)'
            ),
            (
                ['cli.py', '--foo', 'bar'],
                [InputOption('foo', 'f', InputOption.VALUE_REQUIRED)],
                {'foo': 'bar'},
                '.parse() parses long options with a required value (with a space separator)'
            ),
            (
                ['cli.py', '-f'],
                [InputOption('foo', 'f')],
                {'foo': True},
                '.parse() parses short options without a value'
            ),
            (
                ['cli.py', '-fbar'],
                [InputOption('foo', 'f', InputOption.VALUE_REQUIRED)],
                {'foo': 'bar'},
                '.parse() parses short options with a required value (with no separator)'
            ),
            (
                ['cli.py', '-f', 'bar'],
                [InputOption('foo', 'f', InputOption.VALUE_REQUIRED)],
                {'foo': 'bar'},
                '.parse() parses short options with a required value (with a space separator)'
            ),
            (
                ['cli.py', '-f', ''],
                [InputOption('foo', 'f', InputOption.VALUE_OPTIONAL)],
                {'foo': None},
                '.parse() parses short options with an optional empty value'
            ),
            (
                ['cli.py', '-f', '', 'foo'],
                [
                    InputArgument('name'),
                    InputOption('foo', 'f', InputOption.VALUE_OPTIONAL)
                ],
                {'foo': None},
                '.parse() parses short options with an optional empty value followed by an argument'
            ),
            (
                ['cli.py', '-f', '', '-b'],
                [
                    InputOption('foo', 'f', InputOption.VALUE_OPTIONAL),
                    InputOption('bar', 'b')
                ],
                {'foo': None, 'bar': True},
                '.parse() parses short options with an optional empty value followed by an option'
            ),
            (
                ['cli.py', '-f', '-b', 'foo'],
                [
                    InputArgument('name'),
                    InputOption('foo', 'f', InputOption.VALUE_OPTIONAL),
                    InputOption('bar', 'b')
                ],
                {'foo': None, 'bar': True},
                '.parse() parses long options with an optional value which is not present'
            ),
            (
                ['cli.py', '-fb'],
                [
                    InputOption('foo', 'f'),
                    InputOption('bar', 'b')
                ],
                {'foo': True, 'bar': True},
                '.parse() parses short options when they are aggregated as a single one'
            ),
            (
                ['cli.py', '-fb', 'bar'],
                [
                    InputOption('foo', 'f'),
                    InputOption('bar', 'b', InputOption.VALUE_REQUIRED)
                ],
                {'foo': True, 'bar': 'bar'},
                '.parse() parses short options when they are aggregated as a single one '
                'and the last one has a required value'
            ),
            (
                ['cli.py', '-fb', 'bar'],
                [
                    InputOption('foo', 'f'),
                    InputOption('bar', 'b', InputOption.VALUE_OPTIONAL)
                ],
                {'foo': True, 'bar': 'bar'},
                '.parse() parses short options when they are aggregated as a single one '
                'and the last one has an optional value'
            ),
            (
                ['cli.py', '-fbbar'],
                [
                    InputOption('foo', 'f'),
                    InputOption('bar', 'b', InputOption.VALUE_OPTIONAL)
                ],
                {'foo': True, 'bar': 'bar'},
                '.parse() parses short options when they are aggregated as a single one '
                'and the last one has a required value with no separator'
            ),
            (
                ['cli.py', '-fbbar'],
                [
                    InputOption('foo', 'f', InputOption.VALUE_OPTIONAL),
                    InputOption('bar', 'b', InputOption.VALUE_OPTIONAL)
                ],
                {'foo': 'bbar', 'bar': None},
                '.parse() parses short options when they are aggregated as a single one '
                'and one of them takes a value'
            )
        ]

    def test_invalid_input(self):
        for argv, definition, expected_exception_message in self.provide_invalid_input():
            input_ = ArgvInput(argv)
            self.assertRaisesRegexp(
                Exception,
                expected_exception_message,
                input_.bind,
                definition
            )

    def provide_invalid_input(self):
        return [
            (
                ['cli.py', '--foo'],
                InputDefinition([
                    InputOption('foo', 'f', InputOption.VALUE_REQUIRED)
                ]),
                'The "--foo" option requires a value.'
            ),
            (
                ['cli.py', '-f'],
                InputDefinition([
                    InputOption('foo', 'f', InputOption.VALUE_REQUIRED)
                ]),
                'The "--foo" option requires a value.'
            ),
            (
                ['cli.py', '-ffoo'],
                InputDefinition([
                    InputOption('foo', 'f', InputOption.VALUE_NONE)
                ]),
                'The "-o" option does not exist.'
            ),
            (
                ['cli.py', '--foo=bar'],
                InputDefinition([
                    InputOption('foo', 'f', InputOption.VALUE_NONE)
                ]),
                'The "--foo" option does not accept a value.'
            ),
            (
                ['cli.py', 'foo', 'bar'],
                InputDefinition(),
                'Too many arguments.'
            ),
            (
                ['cli.py', '--foo'],
                InputDefinition(),
                'The "--foo" option does not exist.'
            ),
            (
                ['cli.py', '-f'],
                InputDefinition(),
                'The "-f" option does not exist.'
            ),
            (
                ['cli.py', '-1'],
                InputDefinition([
                    InputArgument('number')
                ]),
                'The "-1" option does not exist.'
            )
        ]

    def test_parse_list_argument(self):
        input_ = ArgvInput(['cli.py', 'foo', 'bar', 'baz', 'bat'])
        input_.bind(
            InputDefinition([
                InputArgument('name', InputArgument.IS_LIST)
            ])
        )

        self.assertEqual(
            {'name': ['foo', 'bar', 'baz', 'bat']},
            input_.get_arguments()
        )

    def test_parse_list_option(self):
        input_ = ArgvInput(['cli.py', '--name=foo', '--name=bar', '--name=baz'])
        input_.bind(
            InputDefinition([
                InputOption('name', None, InputOption.VALUE_OPTIONAL | InputOption.VALUE_IS_LIST)
            ])
        )
        self.assertEqual(
            {'name': ['foo', 'bar', 'baz']},
            input_.get_options()
        )

        input_ = ArgvInput(['cli.py', '--name', 'foo', '--name', 'bar', '--name', 'baz'])
        input_.bind(
            InputDefinition([
                InputOption('name', None, InputOption.VALUE_OPTIONAL | InputOption.VALUE_IS_LIST)
            ])
        )
        self.assertEqual(
            {'name': ['foo', 'bar', 'baz']},
            input_.get_options()
        )

        input_ = ArgvInput(['cli.py', '--name=foo', '--name=bar', '--name='])
        input_.bind(
            InputDefinition([
                InputOption('name', None, InputOption.VALUE_OPTIONAL | InputOption.VALUE_IS_LIST)
            ])
        )
        self.assertEqual(
            {'name': ['foo', 'bar', None]},
            input_.get_options()
        )

        input_ = ArgvInput(['cli.py', '--name', 'foo', '--name', 'bar', '--name', '--another-option'])
        input_.bind(
            InputDefinition([
                InputOption('name', None, InputOption.VALUE_OPTIONAL | InputOption.VALUE_IS_LIST),
                InputOption('another-option', None, InputOption.VALUE_NONE)
            ])
        )
        self.assertEqual(
            {'name': ['foo', 'bar', None], 'another-option': True},
            input_.get_options()
        )

    def test_negative_number_after_double_dash(self):
        input_ = ArgvInput(['cli.py', '--', '-1'])
        input_.bind(
            InputDefinition([
                InputArgument('number')
            ])
        )
        self.assertEqual({'number': '-1'}, input_.get_arguments())

        input_ = ArgvInput(['cli.py', '-f', 'bar', '--', '-1'])
        input_.bind(
            InputDefinition([
                InputArgument('number'),
                InputOption('foo', 'f', InputOption.VALUE_OPTIONAL)
            ])
        )
        self.assertEqual({'foo': 'bar'}, input_.get_options())
        self.assertEqual({'number': '-1'}, input_.get_arguments())

    def test_parse_empty_string_argument(self):
        input_ = ArgvInput(['cli.py', '-f', 'bar', ''])
        input_.bind(InputDefinition([
            InputArgument('empty'),
            InputOption('foo', 'f', InputOption.VALUE_OPTIONAL)
        ]))
        self.assertEqual({'empty': ''}, input_.get_arguments())

    def test_get_first_argument(self):
        input_ = ArgvInput(['cli.py', '-fbbar'])
        self.assertEqual(None, input_.get_first_argument())

        input_ = ArgvInput(['cli.py', '-fbbar', 'foo'])
        self.assertEqual('foo', input_.get_first_argument())

    def test_has_parameter_option(self):
        input_ = ArgvInput(['cli.py', '-f', 'foo'])
        self.assertTrue(input_.has_parameter_option('-f'))

        input_ = ArgvInput(['cli.py', '--foo', 'foo'])
        self.assertTrue(input_.has_parameter_option('--foo'))

        input_ = ArgvInput(['cli.py', 'foo'])
        self.assertFalse(input_.has_parameter_option('--foo'))

        input_ = ArgvInput(['cli.py', '--foo=bar'])
        self.assertTrue(input_.has_parameter_option('--foo'))

    def test_to_str(self):
        input_ = ArgvInput(['cli.py', '-f', 'foo'])
        self.assertEqual('-f foo', str(input_))

        input_ = ArgvInput(['cli.py', '-f', '--bar=foo', 'a b c d', "A\nB'C"])

        def escape(s):
            return "\\'".join("'" + p + "'" for p in s.split("'"))

        self.assertEqual(
            '-f --bar=foo ' + escape('a b c d') + ' ' + escape("A\nB'C"),
            str(input_)
        )

    def test_get_parameter_option_equal_sign(self):
        for argv, key, expected in self.get_parameter_option_values():
            input_ = ArgvInput(argv)
            self.assertEqual(expected, input_.get_parameter_option(key))

    def get_parameter_option_values(self):
        return [
            (
                ['app/console', 'foo:bar', '-e', 'dev'],
                '-e',
                'dev'
            ),
            (
                ['app/console', 'foo:bar', '--env=dev'],
                '--env',
                'dev'
            ),
            (
                ['app/console', 'foo:bar', '-e', 'dev'],
                ['-e', '--env'],
                'dev'
            ),
            (
                ['app/console', 'foo:bar', '--env=dev'],
                ['-e', '--env'],
                'dev'
            ),
            (
                ['app/console', 'foo:bar', '--env=dev', '--en=1'],
                ['--en'],
                '1'
            )
        ]

    def test_parse_single_dash_argument(self):
        input_ = ArgvInput(['cli.py', '-'])
        input_.bind(InputDefinition([
            InputArgument('file')
        ]))
        self.assertEqual({'file': '-'}, input_.get_arguments())
