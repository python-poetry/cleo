# -*- coding: utf-8 -*-

import re

from .base_command import BaseCommand, CommandError
from ..inputs.list_input import ListInput
from ..parser import Parser
from ..styles import CleoStyle
from ..outputs import Output, NullOutput
from ..questions import Question, ChoiceQuestion, ConfirmationQuestion
from ..helpers import Table
from ..helpers.table_separator import TableSeparator
from ..helpers.table_cell import TableCell
from ..helpers.table_style import TableStyle
from ..helpers.progress_indicator import ProgressIndicator


class Command(BaseCommand):

    name = None

    signature = None

    description = ''

    help = ''

    verbosity = Output.VERBOSITY_NORMAL

    verbosity_map = {
        'v': Output.VERBOSITY_VERBOSE,
        'vv': Output.VERBOSITY_VERY_VERBOSE,
        'vvv': Output.VERBOSITY_DEBUG,
        'quiet': Output.VERBOSITY_QUIET,
        'normal': Output.VERBOSITY_NORMAL
    }

    validation = None

    hidden = False

    def __init__(self, name=None):
        self.input = None
        self.output = None
        doc = self.__doc__ or super(self.__class__, self).__doc__

        if doc:
            self._parse_doc(doc)

        if not self.signature:
            parent = super(self.__class__, self)
            if hasattr(parent, 'signature'):
                self.signature = parent.signature

        if self.signature:
            self._configure_using_fluent_definition()
        else:
            super(Command, self).__init__(name or self.name)

    def _parse_doc(self, doc):
        doc = doc.strip().split('\n', 1)
        if len(doc) > 1:
            self.description = doc[0].strip()
            self.signature = re.sub('\s{2,}', ' ', doc[1].strip())
        else:
            self.description = doc[0].strip()

    def _configure_using_fluent_definition(self):
        """
        Configure the console command using a fluent definition.
        """
        definition = Parser.parse(self.signature)

        super(Command, self).__init__(definition['name'])

        for argument in definition['arguments']:
            if self.validation and argument.get_name() in self.validation:
                argument.set_validator(self.validation[argument.get_name()])

            self.get_definition().add_argument(argument)

        for option in definition['options']:
            if self.validation and '--%s' % option.get_name() in self.validation:
                option.set_validator(self.validation['--%s' % option.get_name()])

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

        return command.run(ListInput(options), self.output.output)

    def call_silent(self, name, options=None):
        """
        Call another command silently.

        :param name: The command name
        :type name: str

        :param options: The options
        :type options: list or None
        """
        if options is None:
            options = []

        command = self.get_application().find(name)

        options = [('command', command.get_name())] + options

        return command.run(ListInput(options), NullOutput())

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

    def confirm(self, question, default=False, true_answer_regex='(?i)^y'):
        """
        Confirm a question with the user.

        :param question: The question to ask
        :type question: str

        :param default: The default value
        :type default: bool

        :param true_answer_regex: A regex to match the "yes" answer
        :type true_answer_regex: str

        :rtype: bool
        """
        return self.output.confirm(question, default, true_answer_regex)

    def ask(self, question, default=None):
        """
        Prompt the user for input.

        :param question: The question to ask
        :type question: str

        :param default: The default value
        :type default: str or None

        :rtype: str
        """
        if isinstance(question, Question):
            return self.get_helper('question').ask(self.input, self.output, question)

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

    def create_question(self, question, type=None, **kwargs):
        """
        Returns a Question of specified type.

        :param type: The type of the question
        :type type: str

        :rtype: mixed
        """
        if not type:
            return Question(question, **kwargs)

        if type == 'choice':
            return ChoiceQuestion(question, **kwargs)

        if type == 'confirmation':
            return ConfirmationQuestion(question, **kwargs)

    def table(self, headers=None, rows=None, style='default'):
        """
        Return a Table instance.

        :param headers: The table headers
        :type headers: list

        :param rows: The table rows
        :type rows: list

        :param style: The table style
        :type style: str
        """
        table = Table(self.output)

        if headers:
            table.set_headers(headers)

        if rows:
            table.set_rows(rows)

        table.set_style(style)

        return table

    def render_table(self, headers, rows, style='default'):
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

    def table_separator(self):
        """
        Return a TableSeparator instance.

        :rtype: TableSeparator
        """
        return TableSeparator()

    def table_cell(self, value, **options):
        """
        Return a TableCell instance

        :param value: The cell value
        :type value: str

        :param options: The cell options
        :type options: dict

        :rtype: TableCell
        """
        return TableCell(value, **options)

    def table_style(self):
        """
        Return a TableStyle instance.

        :rtype: TableStyle
        """
        return TableStyle()

    def write(self, text, style=None):
        """
        Writes a string without a new line.
        Useful if you want to use overwrite().

        :param text: The line to write
        :type text: str

        :param style: The style of the string
        :type style: str
        """
        if style:
            styled = '<%s>%s</>' % (style, text)
        else:
            styled = text

        self.output.write(styled, newline=False)

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

    def line_error(self, text, style=None, verbosity=None):
        """
        Write a string as information output to stderr.

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

        self.output.write_error(styled)

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

    def progress_indicator(self, fmt=None, indicator_change_interval=100,
                           indicator_values=None):
        """
        Creates a new progress indicator.

        :param fmt: Indicator format
        :type fmt: str or None

        :param indicator_change_interval: Change interval in milliseconds
        :type indicator_change_interval: int

        :param indicator_values: Animated indicator characters
        :type indicator_values: list or None

        :rtype: ProgressIndicator
        """
        return ProgressIndicator(self.output, fmt, indicator_change_interval, indicator_values)

    def spin(self, start_message, end_message, fmt=None, interval=100, values=None):
        """
        Automatically spin a progress indicator.
        
        :param start_message: The message to display when starting
        :type start_message: str
        
        :param end_message: The message to display when finishing
        :type end_message: str
        
        :param fmt: Indicator format
        :type fmt: str or None

        :param interval: Change interval in milliseconds
        :type interval: int

        :param values: Animated indicator characters
        :type values: list or None

        :rtype: ProgressIndicator
        """
        spinner = ProgressIndicator(self.output, fmt, interval, values)

        return spinner.auto(start_message, end_message)

    def set_style(self, name, fg=None, bg=None, options=None):
        """
        Sets a new style

        :param name: The name of the style
        :type name: str

        :param fg: The foreground color
        :type fg: str

        :param bg: The background color
        :type bg: str

        :param options: The options
        :type options: list
        """
        self.output.get_formatter().add_style(name, fg, bg, options)

    def overwrite(self, text, size=None):
        """
        Overwrites the current line.

        It will not add a new line so use line('')
        if necessary.

        :param text: The text to write.
        :type text: str

        :param size: The number of characters to overwrite.
        :type size: int or None
        """
        self.output.overwrite(text, size=size)

    def is_hidden(self):
        """
        Returns whether the command is hidden or not.

        :rtype: bool
        """
        return self.hidden

    def _parse_verbosity(self, level=None):
        if level in self.verbosity_map:
            level = self.verbosity_map[level]
        elif not isinstance(level, int):
            level = self.verbosity

        return level

    def _execute_code(self, i, o):
        return self._code(self)
