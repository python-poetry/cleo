# -*- coding: utf-8 -*-

import os
from ..helpers import ProgressBar
from ..outputs import Output


class OutputStyle(Output):
    """
    Decorates output to add console style guide helpers.
    """

    def __init__(self, output):
        """
        Constructor.

        @param output: An Output instance
        @type output: Output
        """
        self._output = output

    def title(self, message):
        """
        Formats a command title.

        @type message: str
        """
        raise NotImplementedError()

    def section(self, message):
        """
        Formats a section title.

        @type message: str
        """
        raise NotImplementedError()

    def listing(self, elements):
        """
        Formats a list.

        @type elements: list
        """
        raise NotImplementedError()

    def text(self, message):
        """
        Formats informational text.

        @type message: str or list
        """
        raise NotImplementedError()

    def success(self, message):
        """
        Formats a success result bar.

        @type message: str or list
        """
        raise NotImplementedError()

    def error(self, message):
        """
        Formats an error result bar.

        @type message: str or list
        """
        raise NotImplementedError()

    def warning(self, message):
        """
        Formats a warning result bar.

        @type message: str or list
        """
        raise NotImplementedError()

    def note(self, message):
        """
        Formats a note admonition.

        @type message: str or list
        """
        raise NotImplementedError()

    def caution(self, message):
        """
        Formats a caution admonition.

        @type message: str or list
        """
        raise NotImplementedError()

    def table(self, headers, rows):
        """
        Formats a table.

        @type headers: list
        @type rows: list
        """
        raise NotImplementedError()

    def ask(self, question, default=None, validator=None):
        """
        Asks a question

        @type question: str
        @type default: str or None
        @type validator: callable or None

        @rtype: str
        """
        raise NotImplementedError()

    def ask_hidden(self, question, validator=None):
        """
        Asks a question with the user input hidden.

        @type question: str
        @type validator: callable or None

        @rtype: str
        """
        raise NotImplementedError()

    def confirm(self, question, default=True):
        """
        Asks for confirmation.

        @type question: str
        @type default: bool

        @rtype: bool
        """
        raise NotImplementedError()

    def choice(self, question, choices, default=None):
        """
        Asks a choice question.

        @type question: str
        @type choices: list
        @type default: str or int or None

        @rtype: str
        """
        raise NotImplementedError()

    def new_line(self, count=1):
        """
        Add newline(s).

        @param count: The number of newlines
        @type count: int
        """
        self._output.write(os.linesep * count)

    def create_progress_bar(self, max=0):
        """
        Create a new progress bar

        @int max: int

        @rtype ProgressHelper
        """
        return ProgressBar(self, max)

    def write(self, messages, newline=False, type=Output.OUTPUT_NORMAL):
        self._output.write(messages, newline, type)

    def writeln(self, messages, type=Output.OUTPUT_NORMAL):
        self._output.writeln(messages, type)

    def set_formatter(self, formatter):
        self._output.set_formatter(formatter)

    def get_formatter(self):
        return self._output.get_formatter()

    def set_decorated(self, decorated):
        self._output.get_formatter().set_decorated(bool(decorated))

    def is_decorated(self):
        return self._output.is_decorated()

    def set_verbosity(self, level):
        self._output.set_verbosity(level)

    def get_verbosity(self):
        return self._output.get_verbosity()

    def is_quiet(self):
        return self._output.is_quiet()

    def is_verbose(self):
        return self._output.is_verbose()

    def is_very_verbose(self):
        return self._output.is_very_verbose()

    def is_debug(self):
        return self._output.is_debug()
