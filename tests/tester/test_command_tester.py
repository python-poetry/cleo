# -*- coding: utf-8 -*-

from unittest import TestCase
from cleo.tester.command_tester import CommandTester
from cleo.command.command import Command
from cleo.output.output import Output


class TestCommandTester(TestCase):

    def setUp(self):
        self.command = Command('foo')
        self.command.add_argument('command')
        self.command.add_argument('foo')
        self.command.set_code(lambda input_, output_: output_.writeln('foo'))

        self.tester = CommandTester(self.command)
        self.tester.execute([('foo', 'bar')],
                            {'interactive': False,
                             'decorated': False,
                             'verbosity': Output.VERBOSITY_VERBOSE})

    def tearDown(self):
        self.command = None
        self.tester = None

    def test_execute(self):
        """
        CommandTester.execute() behaves properly
        """
        self.assertFalse(self.tester.get_input().is_interactive(),
                         msg='.execute() takes an interactive option.')
        self.assertFalse(self.tester.get_output().is_decorated(),
                         msg='.execute() takes a decorated option.')
        self.assertEqual(Output.VERBOSITY_VERBOSE, self.tester.get_output().get_verbosity(),
                         msg='.execute() takes an interactive option.')

    def test_get_input(self):
        """
        CommandTester.get_input() behaves properly
        """
        self.assertEqual('bar', self.tester.get_input().get_argument('foo'),
                         msg='.get_input() returns the current input instance.')

    def test_get_output(self):
        """
        CommandTester.get_input() behaves properly
        """
        self.tester.get_output().get_stream().seek(0)
        self.assertEqual('foo\n', self.tester.get_output().get_stream().read(),
                         msg='.get_output() returns the current output instance.')

    def test_get_display(self):
        """
        CommandTester.get_display() behaves properly
        """
        self.assertEqual('foo\n', self.tester.get_display(),
                         msg='.get_display() returns the display of the last execution.')
