# -*- coding: utf-8 -*-

import sys
from cleo.application import Application
from cleo.commands import Command, HelpCommand
from cleo.outputs import Output, NullOutput, StreamOutput
from cleo.inputs import InputArgument, InputOption, ListInput, InputDefinition
from cleo.testers.application_tester import ApplicationTester
from cleo.helpers import HelperSet, FormatterHelper

from . import CleoTestCase
from .fixtures.foo_command import FooCommand, foo_commmand, foo_code
from .fixtures.foo1_command import Foo1Command
from .fixtures.foo2_command import Foo2Command
from .fixtures.foo3_command import Foo3Command
from .fixtures.foo4_command import Foo4Command
from .fixtures.foo5_command import Foo5Command
from .fixtures.foobar_command import FoobarCommand
from .fixtures.bar_buc_command import BarBucCommand


class ApplicationTest(CleoTestCase):

    def ensure_static_command_help(self, application):
        for command in application.all().values():
            command.set_help(
                command.get_help().replace(
                    '%command.full_name%',
                    'app/console %command.name%'
                )
            )

    def test_constructor(self):
        """
        Application.__init__() behaves properly
        """
        application = Application('foo', 'bar')

        self.assertEqual('foo',
                         application.get_name(),
                         msg='__init__() takes the application name as its first argument')
        self.assertEqual('bar',
                         application.get_version(),
                         msg='__init__() takes the application version as its second argument')
        self.assertEqual(['help', 'list'].sort(),
                         list(application.all().keys()).sort(),
                         msg='__init__() registered the help and list commands by default')

    def test_set_get_name(self):
        """
        Application name accessors behave properly
        """
        application = Application()
        application.set_name('foo')

        self.assertEqual('foo',
                         application.get_name(),
                         msg='.set_name() sets the name of the application')

    def test_set_get_version(self):
        """
        Application version accessors behave properly
        """
        application = Application()
        application.set_version('bar')

        self.assertEqual('bar',
                         application.get_version(),
                         msg='.set_version() sets the version of the application')

    def test_get_long_version(self):
        """
        Application.get_long_version() returns the long version of the application
        """
        application = Application('foo', 'bar')

        self.assertEqual(
            '<info>foo</info> version <comment>bar</comment>',
            application.get_long_version()
        )

    def test_help(self):
        """
        Application.get_help() returns the help message of the application
        """
        application = Application()

        self.assertEqual(
            self.open_fixture('application_gethelp.txt'),
            application.get_help()
        )

    def test_all(self):
        """
        Application.get_all() returns all comands of the application
        """
        application = Application()
        commands = application.all()

        self.assertEqual(
            'HelpCommand',
            commands['help'].__class__.__name__,
            msg='.all() returns the registered commands'
        )

        application.add(FooCommand())

        self.assertEqual(
            1,
            len(application.all('foo')),
            msg='.all() take a namespace as first argument'
        )

    def test_register(self):
        """
        Application.register() registers a new command
        """
        application = Application()
        command = application.register('foo')

        self.assertEqual(
            'foo',
            command.get_name(),
            msg='.register() registers a new command'
        )

    def test_add(self):
        """
        Application.add() and .addCommands() register commands
        """
        application = Application()
        foo = FooCommand()
        application.add(foo)

        self.assertEqual(
            foo,
            application.all()['foo:bar'],
            msg='.add() registers a command'
        )

        application = Application()
        foo, foo1 = FooCommand(), Foo1Command()
        application.add_commands([foo, foo1])
        commands = application.all()

        self.assertEqual(
            [foo, foo1],
            [commands['foo:bar'], commands['foo:bar1']],
            msg='.add_commands() registers a list of commands'
        )

    def test_add_command_with_empty_constructor(self):
        """
        Application.add() should raise an exception when command constructor is empty
        """
        application = Application()

        self.assertRaisesRegexp(
            Exception,
            'Command class "Foo5Command" is not correctly initialized\.'
            'You probably forgot to call the parent constructor\.',
            application.add,
            Foo5Command()
        )

    def test_add_with_dictionary(self):
        """
        Application.add() accepts a dictionary as argument.
        """
        application = Application()

        foo = application.add(foo_commmand)
        self.assertTrue(isinstance(foo, Command))
        self.assertEqual('foo:bar1', foo.get_name())

    def test_has_get(self):
        """
        Application.has() and Application.get() should determine and get commands
        """
        application = Application()

        self.assertTrue(
            application.has('list'),
            msg='.has() returns true if a command is registered'
        )
        self.assertFalse(
            application.has('afoobar'),
            msg='.has() returns false if a command is not registered'
        )

        foo = FooCommand()
        application.add(foo)

        self.assertTrue(
            application.has('afoobar'),
            msg='.has() returns true if an alias is registered'
        )
        self.assertEqual(
            foo,
            application.get('foo:bar'),
            msg='.get() returns a command by name'
        )
        self.assertEqual(
            foo,
            application.get('afoobar'),
            msg='.get() returns a command by alias'
        )

        application = Application()
        application.add(foo)
        # Simulate help
        application._want_helps = True
        self.assertTrue(
            isinstance(application.get('foo:bar'), HelpCommand),
            msg='.get() returns the help command if --help is provided as the input'
        )

    def test_silent_help(self):
        """
        Silent help should return nothing
        """
        application = Application()
        application.set_auto_exit(False)
        application.set_catch_exceptions(False)

        tester = ApplicationTester(application)
        tester.run(
            [('-h', True),
             ('-q', True)],
            {'decorated': False}
        )

        self.assertEqual('', tester.get_display())

    def test_get_invalid_command(self):
        """
        Application.get() should raise an exception when command does not exist
        """
        application = Application()
        self.assertRaisesRegexp(
            Exception,
            'The command "foofoo" does not exist',
            application.get,
            'foofoo'
        )

    def test_get_namespaces(self):
        """
        Application.get_namespaces() should return registered namespaces
        """
        application = Application()
        application.add(FooCommand())
        application.add(Foo1Command())

        self.assertEqual(
            ['foo'],
            application.get_namespaces(),
            msg='.get_namespaces() returns an array of unique used namespaces'
        )

    def test_find_namespace(self):
        """
        Application.find_namespace() should return a namespace
        """
        application = Application()
        application.add(FooCommand())

        self.assertEqual(
            'foo',
            application.find_namespace('foo'),
            msg='.find_namespace() returns the given namespace if it exists'
        )
        self.assertEqual(
            'foo',
            application.find_namespace('f'),
            msg='.find_namespace() finds a namespace given an abbreviation'
        )

        application.add(Foo2Command())

        self.assertEqual(
            'foo',
            application.find_namespace('foo'),
            msg='.find_namespace() returns the given namespace if it exists'
        )

    def test_find_ambiguous_namespace(self):
        """
        Application.find_namespace() should raise an error when namespace is ambiguous
        """
        application = Application()
        application.add(BarBucCommand())
        application.add(FooCommand())
        application.add(Foo2Command())

        self.assertRaisesRegexp(
            Exception,
            'The namespace "f" is ambiguous \(foo, foo1\)\.',
            application.find_namespace,
            'f'
        )

    def find_invalid_namespace(self):
        """
        Application.find_namespace() should raise an error when finding missing namespace
        """
        application = Application()

        self.assertRaisesRegexp(
            Exception,
            'There are no commands defined in the "bar" namespace\.',
            application.find_namespace,
            'bar'
        )

    def test_find_unique_name_but_namespace_name(self):
        """
        Application.find() should raise an error when command is missing
        """
        application = Application()
        application.add(FooCommand())
        application.add(Foo1Command())
        application.add(Foo2Command())

        self.assertRaisesRegexp(
            Exception,
            'Command "foo1" is not defined',
            application.find,
            'foo1'
        )

    def test_find(self):
        """
        Application.find() should return a command
        """
        application = Application()
        application.add(FooCommand())

        self.assertTrue(
            isinstance(application.find('foo:bar'), FooCommand),
            msg='.find() returns a command if its name exists'
        )
        self.assertTrue(
            isinstance(application.find('h'), HelpCommand),
            msg='.find() returns a command if its name exists'
        )
        self.assertTrue(
            isinstance(application.find('f:bar'), FooCommand),
            msg='.find() returns a command if the abbreviation for the namespace exists'
        )
        self.assertTrue(
            isinstance(application.find('f:b'), FooCommand),
            msg='.find() returns a command if the abbreviation for the namespace and the command name exist'
        )
        self.assertTrue(
            isinstance(application.find('a'), FooCommand),
            msg='.find() returns a command if the abbreviation exists for an alias'
        )

    def test_find_with_ambiguous_abbreviations(self):
        """
        Application.find() should raise an error when there is ambiguosity
        """
        data = [
            ['f', 'Command "f" is not defined\.'],
            ['a', 'Command "a" is ambiguous \(afoobar, afoobar1 and 1 more\)\.'],
            ['foo:b', 'Command "foo:b" is ambiguous \(foo1:bar, foo:bar and 1 more\)\.'],
        ]

        application = Application()
        application.add(FooCommand())
        application.add(Foo1Command())
        application.add(Foo2Command())

        for d in data:
            self.assertRaisesRegexp(
                Exception,
                d[1],
                application.find,
                d[0]
            )

    def test_find_command_equal_namesapce(self):
        """
        Application.find() returns a command if it has a namespace with the same name
        """
        application = Application()
        application.add(Foo3Command())
        application.add(Foo4Command())

        self.assertTrue(
            isinstance(application.find('foo3:bar'), Foo3Command),
            msg='.find() returns the good command even if a namespace has same name'
        )
        self.assertTrue(
            isinstance(application.find('foo3:bar:toh'), Foo4Command),
            msg='.find() returns a command even if its namespace equals another command name'
        )

    def test_find_command_with_ambiguous_namespace_but_unique_name(self):
        """
        Application.find() returns a command with ambiguous namespace
        """
        application = Application()
        application.add(FooCommand())
        application.add(FoobarCommand())

        self.assertTrue(
            isinstance(application.find('f:f'), FoobarCommand)
        )

    def test_find_command_with_missing_namespace(self):
        """
        Application.find() returns a command with missing namespace
        """
        application = Application()
        application.add(Foo4Command())

        self.assertTrue(
            isinstance(application.find('f::t'), Foo4Command)
        )

    def test_find_alternative_exception_message_single(self):
        """
        Application.find() raises an exception when an alternative has been found
        """
        data = [
            'foo3:baR',
            'foO3:bar'
        ]

        application = Application()
        application.add(Foo3Command())

        for d in data:
            self.assertRaisesRegexp(
                Exception,
                'Did you mean this',
                application.find,
                d
            )

    def test_find_alternative_exception_message_multiple(self):
        """
        Application.find() raises an exception when alternatives have been found
        """
        application = Application()
        application.add(FooCommand())
        application.add(Foo1Command())
        application.add(Foo2Command())

        try:
            application.find('foo:baR')
            self.fail('.find() raises an Exception if command does not exist, with alternatives')
        except Exception as e:
            self.assertRegexpMatches(
                str(e),
                'Did you mean one of these'
            )
            self.assertRegexpMatches(
                str(e),
                'foo1:bar'
            )
            self.assertRegexpMatches(
                str(e),
                'foo:bar'
            )

        try:
            application.find('foo2:baR')
            self.fail('.find() raises an Exception if command does not exist, with alternatives')
        except Exception as e:
            self.assertRegexpMatches(
                str(e),
                'Did you mean one of these'
            )
            self.assertRegexpMatches(
                str(e),
                'foo1'
            )

        application.add(Foo3Command())
        application.add(Foo4Command())

        try:
            application.find('foo3:')
            self.fail('.find() raises an Exception if command does not exist, with alternatives')
        except Exception as e:
            self.assertRegexpMatches(
                str(e),
                'foo3:bar'
            )
            self.assertRegexpMatches(
                str(e),
                'foo3:bar:toh'
            )

    def test_find_alternative_commands(self):
        application = Application()
        application.add(FooCommand())
        application.add(Foo1Command())
        application.add(Foo2Command())

        command_name = 'Unknown command'
        try:
            application.find(command_name)
            self.fail('.find() raises an Exception if command does not exist')
        except Exception as e:
            self.assertEqual(
                'Command "%s" is not defined.' % command_name,
                str(e)
            )

        command_name = 'bar1'
        try:
            application.find(command_name)
            self.fail('.find() raises an Exception if command does not exist')
        except Exception as e:
            self.assertRegexpMatches(
                str(e),
                'Command "%s" is not defined.' % command_name
            )
            self.assertRegexpMatches(
                str(e),
                'afoobar1',
            )
            self.assertRegexpMatches(
                str(e),
                'foo:bar1',
            )
            self.assertNotRegex(
                str(e),
                'foo:bar$'
            )

    def find_alternative_commands_with_an_alias(self):
        foo_command = FooCommand()
        foo_command.set_aliases(['foo2'])

        application = Application()
        application.add(foo_command)

        result = application.find('foo')

        self.assertEqual(foo_command, result)

    def test_find_alternative_namespace(self):
        application = Application()

        application.add(FooCommand())
        application.add(Foo1Command())
        application.add(Foo2Command())
        application.add(Foo3Command())

        try:
            application.find('Unknown-namespace:Unknown-command')
            self.fail('.find() raises an Exception if namespace does not exist')
        except Exception as e:
            self.assertRegex(
                str(e),
                'There are no commands defined in the "Unknown-namespace" namespace.'
            )

        try:
            application.find('foo2:command')
            self.fail('.find() raises an tException if namespace does not exist')
        except Exception as e:
            self.assertRegex(
                str(e),
                'There are no commands defined in the "foo2" namespace.'
            )
            self.assertRegex(
                str(e),
                'foo',
                msg='.find() raises an tException if namespace does not exist, with alternative "foo"'
            )
            self.assertRegex(
                str(e),
                'foo1',
                msg='.find() raises an tException if namespace does not exist, with alternative "foo1"'
            )
            self.assertRegex(
                str(e),
                'foo3',
                msg='.find() raises an Exception if namespace does not exist, with alternative "foo2"'
            )

    def test_find_namespace_does_not_fail_on_deep_similar_namespaces(self):
        applicaton = Application()
        applicaton.get_namespaces = self.mock().MagicMock(return_value=['foo:sublong', 'bar:sub'])

        self.assertEqual(
            'foo:sublong',
            applicaton.find_namespace('f:sub')
        )

    def test_set_catch_exceptions(self):
        application = Application()
        application.set_auto_exit(False)
        application.get_terminal_width = self.mock().MagicMock(return_value=120)
        tester = ApplicationTester(application)

        application.set_catch_exceptions(True)
        tester.run([('command', 'foo')], {'decorated': False})
        self.assertEqual(
            self.open_fixture('application_renderexception1.txt'),
            tester.get_display()
        )

        application.set_catch_exceptions(False)
        try:
            tester.run([('command', 'foo')], {'decorated': False})
            self.fail('.set_catch_exceptions() sets the catch exception flag')
        except Exception as e:
            self.assertEqual('Command "foo" is not defined.', str(e))

    def test_as_text(self):
        """
        Application.as_text() returns a text representation of the application.
        """
        application = Application()
        application.add(FooCommand())

        self.ensure_static_command_help(application)

        self.assertEqual(
            self.open_fixture('application_astext1.txt'),
            application.as_text()
        )
        self.assertEqual(
            self.open_fixture('application_astext2.txt'),
            application.as_text('foo')
        )

    def test_render_exception(self):
        """
        Application.render_exception() displays formatted exception.
        """
        application = Application()
        application.set_auto_exit(False)

        application.get_terminal_width = self.mock().MagicMock(return_value=120)
        tester = ApplicationTester(application)

        tester.run([('command', 'foo')], {'decorated': False})
        self.assertEqual(
            self.open_fixture('application_renderexception1.txt'),
            tester.get_display()
        )

        tester.run([('command', 'foo')],
                   {'decorated': False, 'verbosity': Output.VERBOSITY_VERBOSE})
        self.assertRegex(
            tester.get_display(),
            'Exception trace'
        )

        tester.run([('command', 'list'), ('--foo', True)], {'decorated': False})
        self.assertEqual(
            self.open_fixture('application_renderexception2.txt'),
            tester.get_display()
        )

        application.add(Foo3Command())
        tester = ApplicationTester(application)
        tester.run([('command', 'foo3:bar')], {'decorated': False})
        self.assertEqual(
            self.open_fixture('application_renderexception3.txt'),
            tester.get_display()
        )
        tester = ApplicationTester(application)
        tester.run([('command', 'foo3:bar')], {'decorated': True})
        self.assertEqual(
            self.open_fixture('application_renderexception3decorated.txt'),
            tester.get_display()
        )


        application = Application()
        application.set_auto_exit(False)

        application.get_terminal_width = self.mock().MagicMock(return_value=31)
        tester = ApplicationTester(application)

        tester.run([('command', 'foo')], {'decorated': False})
        self.assertEqual(
            self.open_fixture('application_renderexception4.txt'),
            tester.get_display()
        )


    def test_run(self):
        application = Application()
        application.set_auto_exit(False)
        application.set_catch_exceptions(False)
        command = Foo1Command()
        application.add(command)

        sys.argv = ['cli.py', 'foo:bar1']

        application.run()

        self.assertEqual(
            'ArgvInput',
            command.input.__class__.__name__
        )
        self.assertEqual(
            'ConsoleOutput',
            command.output.__class__.__name__
        )

        application = Application()
        application.set_auto_exit(False)
        application.set_catch_exceptions(False)

        self.ensure_static_command_help(application)
        tester = ApplicationTester(application)

        tester.run([], {'decorated': False})
        self.assertEqual(
            self.open_fixture('application_run1.txt'),
            tester.get_display()
        )

        tester.run([('--help', True)], {'decorated': False})
        self.assertEqual(
            self.open_fixture('application_run2.txt'),
            tester.get_display()
        )

        tester.run([('-h', True)], {'decorated': False})
        self.assertEqual(
            self.open_fixture('application_run2.txt'),
            tester.get_display()
        )

        tester.run([('command', 'list'), ('--help', True)], {'decorated': False})
        self.assertEqual(
            self.open_fixture('application_run3.txt'),
            tester.get_display()
        )

        tester.run([('command', 'list'), ('-h', True)], {'decorated': False})
        self.assertEqual(
            self.open_fixture('application_run3.txt'),
            tester.get_display()
        )

        tester.run([('--ansi', True)])
        self.assertTrue(tester.get_output().is_decorated())

        tester.run([('--no-ansi', True)])
        self.assertFalse(tester.get_output().is_decorated())

        tester.run([('--version', True)], {'decorated': False})
        self.assertEqual(
            self.open_fixture('application_run4.txt'),
            tester.get_display()
        )

        tester.run([('-V', True)], {'decorated': False})
        self.assertEqual(
            self.open_fixture('application_run4.txt'),
            tester.get_display()
        )

        tester.run([('command', 'list'), ('--quiet', True)])
        self.assertEqual(
            '',
            tester.get_display()
        )

        tester.run([('command', 'list'), ('-q', True)])
        self.assertEqual(
            '',
            tester.get_display()
        )

        tester.run([('command', 'list'), ('--verbose', True)])
        self.assertEqual(
            Output.VERBOSITY_VERBOSE,
            tester.get_output().get_verbosity()
        )

        tester.run([('command', 'list'), ('-v', True)])
        self.assertEqual(
            Output.VERBOSITY_VERBOSE,
            tester.get_output().get_verbosity()
        )

        application = Application()
        application.set_auto_exit(False)
        application.set_catch_exceptions(False)
        application.add(FooCommand())
        tester = ApplicationTester(application)

        tester.run([('command', 'foo:bar'), ('--no-interaction', True)], {'decorated': False})
        self.assertEqual(
            'called\n',
            tester.get_display()
        )

        tester.run([('command', 'foo:bar'), ('-n', True)], {'decorated': False})
        self.assertEqual(
            'called\n',
            tester.get_display()
        )

    def test_run_returns_integer_exit_code(self):
        exception = OSError(4, '')

        application = Application()
        application.set_auto_exit(False)
        application.do_run = self.mock().MagicMock(side_effect=exception)

        exit_code = application.run(ListInput([]), NullOutput())

        self.assertEqual(4, exit_code)

    def test_run_return_exit_code_one_for_exception_code_zero(self):
        exception = OSError(0, '')

        application = Application()
        application.set_auto_exit(False)
        application.do_run = self.mock().MagicMock(side_effect=exception)

        exit_code = application.run(ListInput([]), NullOutput())

        self.assertEqual(1, exit_code)

    def test_adding_already_set_definition_element_data(self):
        data = [
            [InputArgument('command', InputArgument.REQUIRED)],
            [InputOption('quiet', '', InputOption.VALUE_NONE)],
            [InputOption('query', 'q', InputOption.VALUE_NONE)]
        ]

        for d in data:
            application = Application()
            application.set_auto_exit(False)
            application.set_catch_exceptions(False)
            application.register('foo')\
                .set_definition(d)\
                .set_code(lambda in_, out_: None)

            input_ = ListInput([('command', 'foo')])
            output_ = NullOutput()

            self.assertRaises(
                Exception,
                application.run,
                input_,
                output_
            )

    def test_get_default_helper_set_returns_default_values(self):
        application = Application()
        application.set_auto_exit(False)
        application.set_catch_exceptions(False)

        helper_set = application.get_helper_set()

        self.assertTrue(helper_set.has('formatter'))
        self.assertTrue(helper_set.has('dialog'))
        self.assertTrue(helper_set.has('progress'))

    def test_adding_single_helper_set_overwrites_default_values(self):
        application = Application()
        application.set_auto_exit(False)
        application.set_catch_exceptions(False)

        application.set_helper_set(
            HelperSet({
                'formatter': FormatterHelper()
            })
        )

        helper_set = application.get_helper_set()

        self.assertTrue(helper_set.has('formatter'))
        self.assertFalse(helper_set.has('dialog'))
        self.assertFalse(helper_set.has('progress'))

    def test_overwriting_single_helper_set_overwrites_default_values(self):
        application = CustomApplication()
        application.set_auto_exit(False)
        application.set_catch_exceptions(False)

        application.set_helper_set(
            HelperSet({
                'formatter': FormatterHelper()
            })
        )

        helper_set = application.get_helper_set()

        self.assertTrue(helper_set.has('formatter'))
        self.assertFalse(helper_set.has('dialog'))
        self.assertFalse(helper_set.has('progress'))

    def test_get_default_input_definition_returns_default_values(self):
        application = Application()
        application.set_auto_exit(False)
        application.set_catch_exceptions(False)

        definition = application.get_definition()

        self.assertTrue(definition.has_argument('command'))

        self.assertTrue(definition.has_option('help'))
        self.assertTrue(definition.has_option('quiet'))
        self.assertTrue(definition.has_option('verbose'))
        self.assertTrue(definition.has_option('version'))
        self.assertTrue(definition.has_option('ansi'))
        self.assertTrue(definition.has_option('no-ansi'))
        self.assertTrue(definition.has_option('no-interaction'))

    def test_overwriting_input_definition_overwrites_default_values(self):
        application = CustomApplication()
        application.set_auto_exit(False)
        application.set_catch_exceptions(False)

        definition = application.get_definition()

        self.assertFalse(definition.has_argument('command'))

        self.assertFalse(definition.has_option('help'))
        self.assertFalse(definition.has_option('quiet'))
        self.assertFalse(definition.has_option('verbose'))
        self.assertFalse(definition.has_option('version'))
        self.assertFalse(definition.has_option('ansi'))
        self.assertFalse(definition.has_option('no-ansi'))
        self.assertFalse(definition.has_option('no-interaction'))

        self.assertTrue(definition.has_option('custom'))

    def test_setting_input_definition_overwrites_default_values(self):
        application = Application()
        application.set_auto_exit(False)
        application.set_catch_exceptions(False)

        application.set_definition(InputDefinition([
            InputOption('--custom', '-c',
                        InputOption.VALUE_NONE,
                        'Set the custom input definition.')
        ]))

        definition = application.get_definition()

        self.assertFalse(definition.has_argument('command'))

        self.assertFalse(definition.has_option('help'))
        self.assertFalse(definition.has_option('quiet'))
        self.assertFalse(definition.has_option('verbose'))
        self.assertFalse(definition.has_option('version'))
        self.assertFalse(definition.has_option('ansi'))
        self.assertFalse(definition.has_option('no-ansi'))
        self.assertFalse(definition.has_option('no-interaction'))

        self.assertTrue(definition.has_option('custom'))

    def test_terminal_dimensions(self):
        application = Application()
        original_dimensions = application.get_terminal_dimensions(StreamOutput(sys.stdout))
        self.assertEqual(2, len(original_dimensions))

        width = 80
        if original_dimensions[0] == width:
            width = 100

        application.set_terminal_dimensions(width, 80)
        self.assertEqual((width, 80), application.get_terminal_dimensions(StreamOutput(sys.stdout)))

    def test_set_run_custom_default_command(self):
        """
        Application calls the default command.
        """
        application = Application()
        application.set_auto_exit(False)
        command = FooCommand()
        application.add(command)
        application.set_default_command(command.get_name())

        tester = ApplicationTester(application)
        tester.run([])
        self.assertEqual(
            'interact called\ncalled\n',
            tester.get_display()
        )

        application = CustomDefaultCommandApplication()
        application.set_auto_exit(False)

        tester = ApplicationTester(application)
        tester.run([])
        self.assertEqual(
            'interact called\ncalled\n',
            tester.get_display()
        )

    def test_command_decorator(self):
        """
        @Application.command decorator should register a command
        """
        application = Application()

        @application.command('decorated_foo', description='Foo')
        def decorated_foo_code(i, o):
            o.writeln('called')

        self.assertTrue(application.has('decorated_foo'))

        command = application.get('decorated_foo')
        self.assertEqual(command._code, decorated_foo_code)
        self.assertEqual(command.get_description(), 'Foo')
        self.assertTrue('decorated_foo_code' in command.get_aliases())

    def test_argument_decorator(self):
        """
        @Application.argument decorator should register a command with a specific argument
        """
        application = Application()

        @application.argument('foo', description='Foo', required=True, is_list=True)
        def decorated_foo_code(i, o):
            """Foo Description"""
            o.writeln('called')

        self.assertTrue(application.has('decorated_foo_code'))

        command = application.get('decorated_foo_code')
        self.assertEqual(command._code, decorated_foo_code)
        self.assertEqual(command.get_description(), 'Foo Description')

        argument = command.get_definition().get_argument('foo')
        self.assertEqual('Foo', argument.get_description())
        self.assertTrue(argument.is_required())
        self.assertTrue(argument.is_list())

    def test_option_decorator(self):
        """
        @Application.option decorator should register a command with a specific option
        """
        application = Application()

        @application.option('foo', 'f', description='Foo', value_required=True, is_list=True)
        def decorated_foo_code(i, o):
            """Foo Description"""
            o.writeln('called')

        self.assertTrue(application.has('decorated_foo_code'))

        command = application.get('decorated_foo_code')
        self.assertEqual(command._code, decorated_foo_code)
        self.assertEqual(command.get_description(), 'Foo Description')

        option = command.get_definition().get_option('foo')
        self.assertEqual('f', option.get_shortcut())
        self.assertEqual('Foo', option.get_description())
        self.assertTrue(option.is_value_required())
        self.assertTrue(option.is_list())

    def test_combined_decorators(self):
        """
        Combining decorators should register a command with arguments and options
        """
        application = Application()

        @application.command('decorated_foo', description='Foo command')
        @application.argument('foo', description='Foo argument', required=True, is_list=True)
        @application.option('bar', 'b', description='Bar option', value_required=True, is_list=True)
        def decorated_foo_code(i, o):
            """Foo Description"""
            o.writeln('called')

        self.assertTrue(application.has('decorated_foo'))

        command = application.get('decorated_foo')
        self.assertEqual(command._code, decorated_foo_code)
        self.assertEqual(command.get_description(), 'Foo command')
        self.assertTrue('decorated_foo_code' in command.get_aliases())

        argument = command.get_definition().get_argument('foo')
        self.assertEqual('Foo argument', argument.get_description())
        self.assertTrue(argument.is_required())
        self.assertTrue(argument.is_list())

        option = command.get_definition().get_option('bar')
        self.assertEqual('b', option.get_shortcut())
        self.assertEqual('Bar option', option.get_description())
        self.assertTrue(option.is_value_required())
        self.assertTrue(option.is_list())


class CustomApplication(Application):

    def get_default_input_definition(self):
        return InputDefinition([
            InputOption('--custom', '-c',
                        InputOption.VALUE_NONE,
                        'Set the custom input definition.')
        ])

    def get_default_helper_set(self):
        return HelperSet([FormatterHelper()])


class CustomDefaultCommandApplication(Application):

    def __init__(self):
        super(CustomDefaultCommandApplication, self).__init__()

        command = FooCommand()
        self.add(command)
        self.set_default_command(command.get_name())
