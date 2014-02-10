# -*- coding: utf-8 -*-

import os
from unittest import TestCase
from cleo.application import Application
from cleo.command import Command, HelpCommand
from cleo.tester.application_tester import ApplicationTester

from .fixtures.foo_command import FooCommand
from .fixtures.foo1_command import Foo1Command
from .fixtures.foo2_command import Foo2Command
from .fixtures.foo3_command import Foo3Command
from .fixtures.foo4_command import Foo4Command
from .fixtures.foo5_command import Foo5Command
from .fixtures.foobar_command import FoobarCommand
from .fixtures.bar_buc_command import BarBucCommand


class ApplicationTest(TestCase):

    def setUp(self):
        self.fixtures_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'fixtures'
        )

    def open_fixture(self, fixture):
        with open(os.path.join(self.fixtures_path, fixture)) as fh:
            return fh.read()

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

        self.assertEqual('', tester.get_display().decode('utf-8'))

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
