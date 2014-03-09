# -*- coding: utf-8 -*-

from cleo.commands.command import Command, CommandError
from cleo.application import Application
from cleo.inputs.input_definition import InputDefinition
from cleo.inputs.input_argument import InputArgument
from cleo.inputs.input_option import InputOption
from cleo.inputs import ListInput
from cleo.outputs import NullOutput
from cleo.helpers import FormatterHelper
from cleo.testers import CommandTester
from .. import CleoTestCase
from ..fixtures.test_command import TestCommand


class CommandTest(CleoTestCase):

    NON_CALLABLE = None

    def test_init(self):
        """
        Command.__init__() behaves properly
        """
        self.assertRaises(Exception, Command)

        command = Command('foo:bar')
        self.assertEqual(
            'foo:bar',
            command.get_name(),
            msg='__init__() takes the command name as its first argument'
        )

    def test_command_name_cannot_be_empty(self):
        """
        A command name cannot be empty.
        """
        self.assertRaises(
            Exception,
            Command
        )

    def test_set_application(self):
        """
        Command.set_application() sets the current application
        """
        application = Application()
        command = TestCommand()
        command.set_application(application)
        self.assertEqual(application, command.get_application(), msg='.set_application() sets the current application')

    def test_set_get_definition(self):
        """
        Command.get/set_definition properly sets and gets definition
        """
        command = TestCommand()
        definition = InputDefinition()
        ret = command.set_definition(definition)
        self.assertEqual(command, ret, msg='.set_definition() implements a fluent interface')
        self.assertEqual(definition, command.get_definition(),
                         msg='.set_definition() sets the current InputDefinition instance')
        command.set_definition([InputArgument('foo'), InputOption('bar')])
        self.assertTrue(command.get_definition().has_argument('foo'),
                        msg='.set_definition() also takes an array of InputArguments and InputOptions as an argument')
        self.assertTrue(command.get_definition().has_option('bar'),
                        msg='.set_definition() also takes an array of InputArguments and InputOptions as an argument')
        command.set_definition(InputDefinition())

    def test_add_argument(self):
        """
        Command.add_argument() adds an argument to command.
        """
        command = TestCommand()
        ret = command.add_argument('foo')

        self.assertEqual(ret, command)
        self.assertTrue(command.get_definition().has_argument('foo'))

    def test_add_argument_from_dict(self):
        """
        Command.add_argument_from_dict() adds an argument to command.
        """
        command = TestCommand()
        ret = command.add_argument_from_dict({'foo': {}})

        self.assertEqual(ret, command)
        self.assertTrue(command.get_definition().has_argument('foo'))

    def test_add_option(self):
        """
        Command.add_option() adds an option to command.
        """
        command = TestCommand()
        ret = command.add_option('foo')

        self.assertEqual(ret, command)
        self.assertTrue(command.get_definition().has_option('foo'))

    def test_get_namespace_get_name_set_name(self):
        command = TestCommand()
        self.assertEqual('namespace:name', command.get_name())

        command.set_name('foo')
        self.assertEqual('foo', command.get_name())

        ret = command.set_name('foobar:bar')
        self.assertEqual(ret, command)
        self.assertEqual('foobar:bar', command.get_name())

    def test_invalid_command_names(self):
        data = ['', 'foo:']

        command = TestCommand()

        for d in data:
            self.assertRaisesRegexp(
                CommandError,
                'Command name "%s" is invalid.' % d,
                command.set_name,
                d
            )

    def test_set_get_description(self):
        command = TestCommand()

        self.assertEqual('description', command.get_description())

        ret = command.set_description('description1')
        self.assertEqual(ret, command)
        self.assertEqual('description1', command.get_description())

    def test_set_get_help(self):
        command = TestCommand()

        self.assertEqual('help', command.get_help())

        ret = command.set_description('help1')
        self.assertEqual(ret, command)
        self.assertEqual('help1', command.get_description())

    def test_get_processed_help(self):
        command = TestCommand()

        command.set_help('The %command.name% command does... Example: python %command.full_name%.')
        self.assertRegex(
            command.get_processed_help(),
            'The namespace:name command does...'
        )
        self.assertNotRegex(
            command.get_processed_help(),
            '%command.full_name%'
        )

    def test_set_get_aliases(self):
        command = TestCommand()

        self.assertEqual(['name'], command.get_aliases())

        ret = command.set_aliases(['name1'])
        self.assertEqual(ret, command)
        self.assertEqual(['name1'], command.get_aliases())

    def test_get_synposis(self):
        command = TestCommand()
        command.add_argument('foo')
        command.add_option('foo')

        self.assertEqual(
            'namespace:name [--foo] [foo]',
            command.get_synopsis()
        )

    def test_get_helper(self):
        application = Application()
        command = TestCommand()
        command.set_application(application)
        formatter_helper = FormatterHelper()

        self.assertEqual(
            formatter_helper.get_name(),
            command.get_helper('formatter').get_name()
        )

    def test_merge_application_definition(self):
        """
        Command.merge_application_definition() merges command and application.
        """
        application1 = Application()
        application1.get_definition().add_arguments([InputArgument('foo')])
        application1.get_definition().add_options([InputOption('bar')])
        command = TestCommand()
        command.set_application(application1)
        command.set_definition(
            InputDefinition([
                InputArgument('bar'),
                InputOption('foo')
            ])
        )

        command.merge_application_definition()
        self.assertTrue(command.get_definition().has_argument('foo'))
        self.assertTrue(command.get_definition().has_option('foo'))
        self.assertTrue(command.get_definition().has_argument('bar'))
        self.assertTrue(command.get_definition().has_option('bar'))

        # It should not merge the definitions twice
        command.merge_application_definition()
        self.assertEqual(3, command.get_definition().get_argument_count())

    def test_merge_application_definition_without_args_then_with_args_adds_args(self):
        application1 = Application()
        application1.get_definition().add_arguments([InputArgument('foo')])
        application1.get_definition().add_options([InputOption('bar')])
        command = TestCommand()
        command.set_application(application1)
        command.set_definition(InputDefinition())

        command.merge_application_definition(False)
        self.assertFalse(command.get_definition().has_argument('foo'))
        self.assertTrue(command.get_definition().has_option('bar'))

        command.merge_application_definition(True)
        self.assertTrue(command.get_definition().has_argument('foo'))

        # It should not merge the definitions twice
        command.merge_application_definition()
        self.assertEqual(2, command.get_definition().get_argument_count())

    def test_run_interactive(self):
        tester = CommandTester(TestCommand())

        tester.execute([], {'interactive': True})

        self.assertEqual(
            'interact called\nexecute called\n',
            tester.get_display()
        )

    def test_run_non_interactive(self):
        tester = CommandTester(TestCommand())

        tester.execute([], {'interactive': False})

        self.assertEqual(
            'execute called\n',
            tester.get_display()
        )

    def test_execute_method_needs_to_be_overwridden(self):
        command = Command('foo')
        self.assertRaises(
            NotImplementedError,
            command.run,
            ListInput([]),
            NullOutput()
        )

    def test_run_with_invalid_option(self):
        command = TestCommand()
        tester = CommandTester(command)

        self.assertRaises(
            Exception,
            'The "--bar" option does not exist.',
            tester.execute,
            [('--bar', True)]
        )

    def test_run_returns_integer_exit_code(self):
        command = TestCommand()
        exit_code = command.run(ListInput([]), NullOutput())
        self.assertEqual(0, exit_code)

        command = TestCommand()
        command.execute = self.mock().MagicMock(return_value=2.3)
        exit_code = command.run(ListInput([]), NullOutput())
        self.assertEqual(2, exit_code)

    def test_set_code(self):
        command = TestCommand()
        ret = command.set_code(lambda in_, out_: out_.writeln('from the code...'))
        self.assertEqual(ret, command)

        tester = CommandTester(command)
        tester.execute([])
        self.assertEqual(
            'interact called\nfrom the code...\n',
            tester.get_display()
        )

        command = TestCommand()
        command.set_code(self.callable_method)
        tester = CommandTester(command)
        tester.execute([])
        self.assertEqual(
            'interact called\nfrom the code...\n',
            tester.get_display()
        )

    def test_set_code_with_non_callable(self):
        command = TestCommand()

        self.assertRaisesRegexp(
            Exception,
            'Invalid callable provided to Command.setCode().',
            command.set_code,
            self.NON_CALLABLE
        )

    def test_as_text(self):
        command = TestCommand()
        command.set_application(Application())
        tester = CommandTester(command)
        tester.execute([('command', command.get_name())])

        self.assertEqual(
            self.open_fixture('command_astext.txt'),
            command.as_text()
        )

    def test_from_dict(self):
        def foo(input_, output_):
            output_.writeln('foo')

        command_dict = {
            'foo': {
                'description': 'The foo command.',
                'aliases': ['foobar'],
                'help': 'This is help.',
                'arguments': [{
                    'bar': {
                        'description': 'The bar argument.',
                        'required': True,
                        'list': True
                    }
                }],
                'options': [{
                    'baz': {
                        'shortcut': 'b',
                        'description': 'The baz option.',
                        'value_required': False,
                        'list': True,
                        'default': ['default']
                    }
                }],
                'code': foo
            }
        }

        command = Command.from_dict(command_dict)

        self.assertTrue(isinstance(command, Command))
        self.assertEqual('foo', command.get_name())
        self.assertEqual(foo, command._code)
        self.assertEqual(['foobar'], command.get_aliases())
        self.assertTrue(command.get_definition().has_argument('bar'))
        self.assertTrue(command.get_definition().has_option('baz'))

    def callable_method(self, input_, output_):
        output_.writeln('from the code...')
