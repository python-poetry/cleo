# -*- coding: utf-8 -*-

from unittest import TestCase
from cleo.command.command import Command
from cleo.application import Application
from cleo.input.input_definition import InputDefinition
from cleo.input.input_argument import InputArgument
from cleo.input.input_option import InputOption
from ..fixtures.test_command import TestCommand


class CommandTest(TestCase):

    def test_init(self):
        """
        Command.__init__() behaves properly
        """
        self.assertRaises(Exception, Command)

        command = Command('foo:bar')
        self.assertEqual('foo:bar', command.get_name(), msg='__init__() takes the command name as its first argument')

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
