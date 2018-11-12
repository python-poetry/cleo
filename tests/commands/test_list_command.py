# -*- coding: utf-8 -*-

import re

from .. import CleoTestCase
from cleo.testers.command_tester import CommandTester
from cleo.application import Application


class ListCommandTest(CleoTestCase):
    def test_execute(self):
        """
        ListCommand.execute() behaves properly
        """
        application = Application()

        command = application.get("list")

        command_tester = CommandTester(command)
        command_tester.execute([("command", command.get_name())], {"decorated": False})
        self.assertRegex(
            command_tester.get_display(), "help\s{2,}Displays help for a command"
        )

        command_tester.execute([("command", command.get_name()), ("--raw", True)])
        output = """help   Displays help for a command
list   Lists commands

"""
        self.assertEqual(output, command_tester.get_display())
