# -*- coding: utf-8 -*-

from cleo import Command, CommandTester
from .. import CleoTestCase


class CommandTesting(Command):
    """
    Command testing.

    test
        {action : The action to execute.}
    """

    def handle(self):
        action = self.argument('action')

        getattr(self, '_' + action)()

    def _overwrite(self):
        self.write('Processing...')
        self.overwrite('Done!')


class CommandTest(CleoTestCase):

    def test_overwrite(self):
        command = CommandTesting()

        tester = CommandTester(command)
        tester.execute([
            ('action', 'overwrite')
        ])

        print(tester.get_display())

        self.assertRegex(
            tester.get_display(),
            '^Processing...{}Done!        '.format('\x08' * 13)
        )
