# -*- coding: utf-8 -*-

from .command import Command
from ..input.input_argument import InputArgument


class HelpCommand(Command):

    __command = None

    def configure(self):
        self.ignore_validation_errors()

        self.set_name('help')\
            .set_definition([
                InputArgument('command_name', InputArgument.OPTIONAL, 'The command name', 'help')
            ])\
            .set_description('Displays help for a command')\
            .set_help("""The <info>%command.name%</info> command displays help for a given command:

  <info>python %command.full_name% list</info>

To display the list of available commands, please use the <info>list</info> command.""")

    def set_command(self, command):
        self.__command = command

    def execute(self, input_, output_):
        if self.__command is None:
            if input_.get_argument('command_name'):
                self.__command = self.get_application().find(input_.get_argument('command_name'))

        if self.__command is None:
            output_.write(self.get_application().as_text())
        else:
            output_.write(self.__command.as_text())

        self.__command = None
