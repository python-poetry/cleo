# -*- coding: utf-8 -*-

from .command import Command
from ..helpers import DescriptorHelper


class HelpCommand(Command):
    """
    Displays help for a command

    help {command_name=help : The command name}
         {--format=txt : The output format (txt, json, or md)}
         {--raw : To output raw command help}
    """

    help = """The <info>%command.name%</info> command displays help for a given command:

  <info>python %command.full_name% list</info>

You can also output the help in other formats by using the <comment>--format</comment> option:

  <info>python %command.full_name% --format=json list</info>

To display the list of available commands, please use the <info>list</info> command."""

    _command = None

    def set_command(self, command):
        self._command = command

    def handle(self):
        if self._command is None:
            self._command = self.get_application().find(self.argument('command_name'))

        helper = DescriptorHelper()
        helper.describe(
            self.output, self._command,
            format=self.option('format'),
            raw_text=self.option('raw')
        )

        self._command = None
