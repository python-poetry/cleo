# -*- coding: utf-8 -*-

import re

from unittest import TestCase
from cleo.tester.command_tester import CommandTester
from cleo.application import Application


class ListCommandTest(TestCase):

    def test_execute(self):
        """
        ListCommand.execute() behaves properly
        """
        application = Application()

        command = application.get('list')

        command_tester = CommandTester(command)
        command_tester.execute([('command', command.get_name()), ('decorated', False)])
        self.assertTrue(re.match('(?s).*help   Displays help for a command.*', command_tester.get_display()) is not None,
                        msg='.execute() returns a list of available commands')

        command_tester.execute([('command', command.get_name()), ('--raw', True)])
        output = """help   Displays help for a command
list   Lists commands
"""
        self.assertEqual(output, command_tester.get_display())
