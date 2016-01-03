# -*- coding: utf-8 -*-

from .base_command import BaseCommand, CommandError
from ..inputs.list_input import ListInput
from ..parser import Parser
from ..styles import CleoStyle
from ..outputs import Output
from ..questions import ChoiceQuestion
from ..helpers import Table


class Command(BaseCommand):

    name = None

    description = None

    signature = ''

    help = ''

    verbosity = Output.VERBOSITY_NORMAL

    verbosity_map = {
        'v': Output.VERBOSITY_VERBOSE,
        'vv': Output.VERBOSITY_VERY_VERBOSE,
        'vvv': Output.VERBOSITY_DEBUG,
        'quiet': Output.VERBOSITY_QUIET,
        'normal': Output.VERBOSITY_NORMAL
    }

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

    def argument(self, key=None):
        """
        Get the value of a command argument.

        :param key: The argument name
        :type key: str

        :rtype: mixed
        """
        if key is None:
            return self.input.get_arguments()

        return self.input.get_argument(key)

    def option(self, key=None):
        """
        Get the value of a command option.

        :param key: The option name
        :type key: str

        :rtype: mixed
        """
        if key is None:
            return self.input.get_options()

        return self.input.get_option(key)

    def confirm(self, question, default=False):
        """
        Confirm a question with the user.

        :param question: The question to ask
        :type question: str

        :param default: The default value
        :type default: bool

        :rtype: bool
        """
        return self.output.confirm(question, default)

    def ask(self, question, default=None):
        """
        Prompt the user for input.

        :param question: The question to ask
        :type question: str

        :param default: The default value
        :type default: str or None

        :rtype: str
        """
        return self.output.ask(question, default)

    def secret(self, question):
        """
        Prompt the user for input but hide the answer from the console.

        :param question: The question to ask
        :type question: str

        :rtype: str
        """
        return self.output.ask_hidden(question)

    def choice(self, question, choices, default=None, attempts=None, multiple=False):
        """
        Give the user a single choice from an list of answers.

        :param question: The question to ask
        :type question: str

        :param choices: The available choices
        :type choices: list

        :param default: The default value
        :type default: str or None

        :param attempts: The max number of attempts
        :type attempts: int

        :param multiple: Multiselect
        :type multiple: int

        :rtype: str
        """
        question = ChoiceQuestion(question, choices, default)

        question.max_attempts = attempts
        question.multiselect = multiple

        return self.output.ask_question(question)

    def table(self, headers, rows, style='default'):
        """
        Format input to textual table.

        :param headers: The table headers
        :type headers: list

        :param rows: The table rows
        :type rows: list

        :param style: The tbale style
        :type style: str
        """
        table = Table(self.output)

        table.set_style(style).set_headers(headers).set_rows(rows).render()

    def line(self, text, style=None, verbosity=None):
        """
        Write a string as information output.

        :param text: The line to write
        :type text: str

        :param style: The style of the string
        :type style: str

        :param verbosity: The verbosity
        :type verbosity: None or int str
        """
        if style:
            styled = '<%s>%s</>' % (style, text)
        else:
            styled = text

        self.output.writeln(styled)

    def info(self, text):
        """
        Write a string as information output.

        :param text: The line to write
        :type text: str
        """
        self.line(text, 'info')

    def comment(self, text):
        """
        Write a string as comment output.

        :param text: The line to write
        :type text: str
        """
        self.line(text, 'comment')

    def question(self, text):
        """
        Write a string as question output.

        :param text: The line to write
        :type text: str
        """
        self.line(text, 'question')

    def error(self, text, block=False):
        """
        Write a string as error output.

        :param text: The line to write
        :type text: str
        """
        if block:
            return self.output.error(text)

        self.line(text, 'error')

    def warning(self, text):
        """
        Write a string as warning output.

        :param text: The line to write
        :type text: str
        """
        self.output.warning(text)

    def list(self, elements):
        """
        Write a list of elements.

        :param elements: The elements to write a list for
        :type elements: list
        """
        self.output.listing(elements)

    def progress_bar(self, max=0):
        """
        Creates a new progress bar

        :param max: The maximum number of steps
        :type max: int

        :rtype: ProgressBar
        """
        return self.output.create_progress_bar(max)

    def _parse_verbosity(self, level=None):
        if level in self.verbosity_map:
            level = self.verbosity_map[level]
        elif not isinstance(level, int):
            level = self.verbosity

        return level

