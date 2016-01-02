# -*- coding: utf-8 -*-

from .base_command import BaseCommand, CommandError
from ..inputs.list_input import ListInput
from ..parser import Parser
from ..styles import CleoStyle


class Command(BaseCommand):

    name = None

    description = None

    signature = None

    help = ''

    def __init__(self, name=None):
        self.input = None
        self.output = None

        if self.signature:
            self._configure_using_fluent_definition()
        else:
            super(Command, self).__init__(name or self.name)

    def _configure_using_fluent_definition(self):
        """
        Configure the console command using a fluent definition.
        """
        definition = Parser.parse(self.signature)

        super(Command, self).__init__(definition['name'])

        for argument in definition['arguments']:
            self.get_definition().add_argument(argument)

        for option in definition['options']:
            self.get_definition().add_option(option)

    def run(self, i, o):
        """
        Initialize command.

        :type i: cleo.inputs.input.Input
        :type o: cleo.outputs.output.Output
        """
        self.input = i
        self.output = CleoStyle(i, o)
        
        return super(Command, self).run(i, o)

    def execute(self, i, o):
        """
        Executes the command.

        :type i: cleo.inputs.input.Input
        :type o: cleo.outputs.output.Output
        """
        return self.handle()

    def handle(self):
        """
        Executes the command.
        """
        raise NotImplementedError()

    def call(self, name, options=None):
        """
        Call another command.

        :param name: The command name
        :type name: str

        :param options: The options
        :type options: list or None
        """
        if options is None:
            options = []

        command = self.get_application().find(name)

        options = [('command', command.get_name())] + options

        return command.run(ListInput(options), self.output)

    def line(self, text):
        """
        Write a string as information output.

        :param text: The line to write
        :type text: str
        """
        self.output.writeln(text)

    def info(self, text):
        """
        Write a string as information output.

        :param text: The line to write
        :type text: str
        """
        self.line('<info>%s</info>' % text)

    def comment(self, text):
        """
        Write a string as comment output.

        :param text: The line to write
        :type text: str
        """
        self.line('<comment>%s</comment>' % text)

    def question(self, text):
        """
        Write a string as question output.

        :param text: The line to write
        :type text: str
        """
        self.line('<question>%s</question>' % text)

    def error(self, text):
        """
        Write a string as error output.

        :param text: The line to write
        :type text: str
        """
        self.line('<error>%s</error>' % text)

    def argument(self, key=None):
        if key is None:
            return self.input.get_arguments()

        return self.input.get_argument(key)

    def option(self, key=None):
        if key is None:
            return self.input.get_options()

        return self.input.get_option(key)
