import re

from typing import Optional

from clikit.api.args import Args
from clikit.api.args.format import ArgsFormat
from clikit.api.formatter import Style
from clikit.api.io import IO
from clikit.args import StringArgs
from clikit.io import NullIO
from clikit.ui.components import ChoiceQuestion
from clikit.ui.components import ConfirmationQuestion
from clikit.ui.components import ProgressIndicator
from clikit.ui.components import Question
from clikit.ui.components import Table
from clikit.ui.style import TableStyle

from cleo.io import ConsoleIO
from cleo.parser import Parser

from .base_command import BaseCommand


class Command(BaseCommand):

    signature = None

    validation = None

    TABLE_STYLES = {
        "ascii": TableStyle.ascii(),
        "borderless": TableStyle.borderless(),
        "solid": TableStyle.solid(),
        "compact": TableStyle.compact(),
    }

    def __init__(self):
        self._args = Args(ArgsFormat())
        self._io = None
        self._command = None

        super(Command, self).__init__()

        doc = self.__doc__ or super(self.__class__, self).__doc__

        if doc:
            self._parse_doc(doc)

        if not self.signature:
            parent = super(self.__class__, self)
            if hasattr(parent, "signature"):
                self.signature = parent.signature

        if self.signature:
            self._configure_using_fluent_definition()

        self._config.set_handler_method("wrap_handle")

    @property
    def io(self):  # type: () -> ConsoleIO
        return self._io

    def _parse_doc(self, doc):
        doc = doc.strip().split("\n", 1)
        if len(doc) > 1:
            self._config.set_description(doc[0].strip())
            self.signature = re.sub(r"\s{2,}", " ", doc[1].strip())
        else:
            self._config.set_description(doc[0].strip())

    def _configure_using_fluent_definition(self):
        """
        Configure the console command using a fluent definition.
        """
        definition = Parser.parse(self.signature)

        self._config.set_name(definition["name"])

        for name, flags, description, default in definition["arguments"]:
            self._config.add_argument(name, flags, description, default)

        for long_name, short_name, flags, description, default in definition["options"]:
            self._config.add_option(long_name, short_name, flags, description, default)

    def wrap_handle(
        self, args, io, command
    ):  # type: (Args, IO, CliKitCommand) -> Optional[int]
        self._args = args
        self._io = io
        self._command = command

        return self.handle()

    def handle(self):  # type: () -> Optional[int]
        """
        Executes the command.
        """
        raise NotImplementedError()

    def call(self, name, args=None):  # type: (str, Optional[str]) -> int
        """
        Call another command.
        """
        if args is None:
            args = ""

        args = StringArgs(args)
        command = self.application.get_command(name)

        return command.run(args, self.io)

    def call_silent(self, name, args=None):  # type: (str, Optional[str]) -> int
        """
        Call another command.
        """
        if args is None:
            args = ""

        args = StringArgs(args)
        command = self.application.get_command(name)

        return command.run(args, NullIO())

    def argument(self, key=None):
        """
        Get the value of a command argument.
        """
        if key is None:
            return self._args.arguments()

        return self._args.argument(key)

    def option(self, key=None):
        """
        Get the value of a command option.
        """
        if key is None:
            return self._args.options()

        return self._args.option(key)

    def confirm(self, question, default=False, true_answer_regex="(?i)^y"):
        """
        Confirm a question with the user.
        """
        return self._io.confirm(question, default, true_answer_regex)

    def ask(self, question, default=None):
        """
        Prompt the user for input.
        """
        if isinstance(question, Question):
            return self._io.ask_question(question)

        return self._io.ask(question, default)

    def secret(self, question):
        """
        Prompt the user for input but hide the answer from the console.
        """
        return self._io.ask_hidden(question)

    def choice(self, question, choices, default=None, attempts=None, multiple=False):
        """
        Give the user a single choice from an list of answers.
        """
        question = ChoiceQuestion(question, choices, default)

        question.set_max_attempts(attempts)
        question.set_multi_select(multiple)

        return self._io.ask_question(question)

    def create_question(self, question, type=None, **kwargs):
        """
        Returns a Question of specified type.
        """
        if not type:
            return Question(question, **kwargs)

        if type == "choice":
            return ChoiceQuestion(question, **kwargs)

        if type == "confirmation":
            return ConfirmationQuestion(question, **kwargs)

    def table(self, header=None, rows=None, style=None):
        """
        Return a Table instance.
        """
        if style is not None:
            style = self.TABLE_STYLES[style]

        table = Table(style)

        if header:
            table.set_header_row(header)

        if rows:
            table.set_rows(rows)

        return table

    def render_table(self, headers, rows, style=None):
        """
        Format input to textual table.
        """
        table = self.table(headers, rows, style)

        table.render(self._io)

    def write(self, text, style=None):
        """
        Writes a string without a new line.
        Useful if you want to use overwrite().
        """
        if style:
            styled = "<%s>%s</>" % (style, text)
        else:
            styled = text

        self._io.write(styled)

    def line(self, text, style=None, verbosity=None):
        """
        Write a string as information output.
        """
        if style:
            styled = "<%s>%s</>" % (style, text)
        else:
            styled = text

        self._io.write_line(styled, verbosity)

    def line_error(self, text, style=None, verbosity=None):
        """
        Write a string as information output to stderr.
        """
        if style:
            styled = "<%s>%s</>" % (style, text)
        else:
            styled = text

        self._io.error_line(styled, verbosity)

    def info(self, text):
        """
        Write a string as information output.

        :param text: The line to write
        :type text: str
        """
        self.line(text, "info")

    def comment(self, text):
        """
        Write a string as comment output.

        :param text: The line to write
        :type text: str
        """
        self.line(text, "comment")

    def question(self, text):
        """
        Write a string as question output.

        :param text: The line to write
        :type text: str
        """
        self.line(text, "question")

    def progress_bar(self, max=0):
        """
        Creates a new progress bar

        :param max: The maximum number of steps
        :type max: int

        :rtype: ProgressBar
        """
        return self._io.progress_bar(max)

    def progress_indicator(self, fmt=None, interval=100, values=None):
        """
        Creates a new progress indicator.
        """
        return ProgressIndicator(self.io, fmt, interval, values)

    def spin(self, start_message, end_message, fmt=None, interval=100, values=None):
        """
        Automatically spin a progress indicator.
        """
        spinner = ProgressIndicator(self.io, fmt, interval, values)

        return spinner.auto(start_message, end_message)

    def add_style(self, name, fg=None, bg=None, options=None):
        """
        Adds a new style
        """
        style = Style(name)
        if fg is not None:
            style.fg(fg)

        if bg is not None:
            style.bg(bg)

        if options is not None:
            if "bold" in options:
                style.bold()

            if "underline" in options:
                style.underlined()

        self._io.output.formatter.add_style(style)
        self._io.error_output.formatter.add_style(style)

    def overwrite(self, text, size=None):
        """
        Overwrites the current line.

        It will not add a new line so use line('')
        if necessary.
        """
        self._io.overwrite(text, size=size)
