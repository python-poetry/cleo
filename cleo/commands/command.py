import inspect
import re

from typing import TYPE_CHECKING
from typing import Any
from typing import List
from typing import Optional
from typing import Union

from cleo import exceptions
from cleo.cursor import Cursor
from cleo.io.inputs.string_input import StringInput
from cleo.io.io import IO
from cleo.io.null_io import NullIO
from cleo.io.outputs.output import Verbosity
from cleo.parser import Parser

from .base_command import BaseCommand


if TYPE_CHECKING:
    from cleo.ui.progress_bar import ProgressBar
    from cleo.ui.progress_indicator import ProgressIndicator
    from cleo.ui.question import Question


class Command(BaseCommand):

    arguments = []
    options = []

    aliases = []

    usages = []

    commands = []

    def __init__(self):
        self._io: Optional[IO] = None
        super(Command, self).__init__()

    @property
    def io(self):  # type: () -> IO
        return self._io

    def configure(self) -> None:
        if not self.name:
            doc = self.__doc__

            if not doc:
                for base in inspect.getmro(self.__class__):
                    if base.__doc__ is not None:
                        doc = base.__doc__
                        break

            if doc:
                self._parse_doc(doc)

        for argument in self.arguments:
            self._definition.add_argument(argument)

        for option in self.options:
            self._definition.add_option(option)

    def _parse_doc(self, doc):
        doc = doc.strip().split("\n", 1)
        if len(doc) > 1:
            self.description = doc[0].strip()
            signature = re.sub(r"\s{2,}", " ", doc[1].strip())
            definition = Parser.parse(signature)
            self.name = definition["name"]

            for argument in definition["arguments"]:
                self._definition.add_argument(argument)

            for option in definition["options"]:
                self._definition.add_option(option)
        else:
            self.description = doc[0].strip()

    def execute(self, io: IO) -> int:
        self._io = io

        try:
            return self.handle()
        except KeyboardInterrupt:
            return 1

    def handle(self) -> int:
        """
        Executes the command.
        """
        raise NotImplementedError()

    def call(self, name: str, args: Optional[str] = None) -> int:
        """
        Call another command.
        """
        if args is None:
            args = ""

        input = StringInput(args)
        command = self.application.get(name)

        return self.application._run_command(command, self._io.with_input(input))

    def call_silent(self, name, args=None):  # type: (str, Optional[str]) -> int
        """
        Call another command silently.
        """
        if args is None:
            args = ""

        args = StringInput(args)
        command = self.application.get(name)

        return self.application._run_command(command, NullIO(input))

    def argument(self, name: str):
        """
        Get the value of a command argument.
        """
        return self._io.input.argument(name)

    def option(self, name: str):
        """
        Get the value of a command option.
        """
        return self._io.input.option(name)

    def confirm(
        self, question: str, default: bool = False, true_answer_regex: str = "(?i)^y"
    ) -> bool:
        """
        Confirm a question with the user.
        """
        from cleo.ui.confirmation_question import ConfirmationQuestion

        question = ConfirmationQuestion(
            question, default=default, true_answer_regex=true_answer_regex
        )

        return question.ask(self._io)

    def ask(
        self, question: Union[str, "Question"], default: Optional[Any] = None
    ) -> Any:
        """
        Prompt the user for input.
        """
        from cleo.ui.question import Question

        if not isinstance(question, Question):
            question = Question(question, default=default)

        return question.ask(self._io)

    def secret(
        self, question: Union[str, "Question"], default: Optional[Any] = None
    ) -> Any:
        """
        Prompt the user for input but hide the answer from the console.
        """
        from cleo.ui.question import Question

        if not isinstance(question, Question):
            question = Question(question)

        question.hide()

        return question.ask(self._io)

    def choice(
        self,
        question: str,
        choices: List[str],
        default: Optional[Any] = None,
        attempts: Optional[int] = None,
        multiple: bool = False,
    ) -> Any:
        """
        Give the user a single choice from an list of answers.
        """
        from cleo.ui.choice_question import ChoiceQuestion

        question = ChoiceQuestion(question, choices, default)

        question.set_max_attempts(attempts)
        question.set_multi_select(multiple)

        return question.ask(self._io)

    def create_question(self, question, type=None, **kwargs):
        """
        Returns a Question of specified type.
        """
        from cleo.ui.choice_question import ChoiceQuestion
        from cleo.ui.confirmation_question import ConfirmationQuestion
        from cleo.ui.question import Question

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
        from cleo.ui.table import Table

        table = Table(self._io, style=style)

        if header:
            table.set_headers([header])

        if rows:
            table.set_rows(rows)

        return table

    def render_table(self, headers, rows, style=None):
        """
        Format input to textual table.
        """
        table = self.table(headers, rows, style)

        table.render()

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

    def line(
        self,
        text: str,
        style: Optional[str] = None,
        verbosity: Verbosity = Verbosity.NORMAL,
    ):
        """
        Write a string as information output.
        """
        if style:
            styled = "<{}>{}</>".format(style, text)
        else:
            styled = text

        self._io.write_line(styled, verbosity=verbosity)

    def line_error(
        self,
        text: str,
        style: Optional[str] = None,
        verbosity: Verbosity = Verbosity.NORMAL,
    ):
        """
        Write a string as information output to stderr.
        """
        if style:
            styled = "<%s>%s</>" % (style, text)
        else:
            styled = text

        self._io.write_error_line(styled, verbosity)

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

    def progress_bar(self, max: int = 0) -> "ProgressBar":
        """
        Creates a new progress bar
        """
        from cleo.ui.progress_bar import ProgressBar

        return ProgressBar(self._io, max=max)

    def progress_indicator(
        self,
        fmt: Optional[str] = None,
        interval: int = 100,
        values: Optional[List[str]] = None,
    ) -> "ProgressIndicator":
        """
        Creates a new progress indicator.
        """
        from cleo.ui.progress_indicator import ProgressIndicator

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

    def overwrite(self, text):
        """
        Overwrites the current line.

        It will not add a new line so use line('')
        if necessary.
        """
        self._io.overwrite(text)
