# -*- coding: utf-8 -*-

from cleo.testers import CommandTester
from cleo.commands import HelpCommand, ListCommand
from cleo.application import Application
from .. import CleoTestCase


class HelpCommandTest(CleoTestCase):

    def test_execute_for_command_alias(self):
        command = HelpCommand()
        command.set_application(Application())
        tester = CommandTester(command)
        tester.execute([('command_name', 'li')])
        self.assertRegex(
            tester.get_display(),
            'list \[--raw\] \[namespace\]'
        )

    def test_execute_for_command(self):
        command = HelpCommand()
        tester = CommandTester(command)
        command.set_command(ListCommand())
        tester.execute([])
        self.assertRegex(
            tester.get_display(),
            'list \[--raw\] \[namespace\]'
        )

    def test_execute_for_application_command(self):
        application = Application()
        tester = CommandTester(application.get('help'))
        tester.execute([('command_name', 'list')])
        self.assertRegex(
            tester.get_display(),
            'list \[--raw\] \[namespace\]'
        )
