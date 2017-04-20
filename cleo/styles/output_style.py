# -*- coding: utf-8 -*-

import os
from ..helpers import ProgressBar, Helper
from ..outputs import Output, ConsoleOutput


class OutputStyle(Output):
    """
    Decorates output to add console style guide helpers.
    """

    def __init__(self, output):
        """
        Constructor.

        :param output: An Output instance
        :type output: Output
        """
        self._output = output
        self._last_message = ''
        self._last_message_err = ''

    @property
    def output(self):
        return self._output

    def title(self, message):
        """
        Formats a command title.

        :type message: str
        """
        raise NotImplementedError()

    def section(self, message):
        """
        Formats a section title.

        :type message: str
        """
        raise NotImplementedError()

    def listing(self, elements):
        """
        Formats a list.

        :type elements: list
        """
        raise NotImplementedError()

    def text(self, message):
        """
        Formats informational text.

        :type message: str or list
        """
        raise NotImplementedError()

    def success(self, message):
        """
        Formats a success result bar.

        :type message: str or list
        """
        raise NotImplementedError()

    def error(self, message):
        """
        Formats an error result bar.

        :type message: str or list
        """
        raise NotImplementedError()

    def warning(self, message):
        """
        Formats a warning result bar.

        :type message: str or list
        """
        raise NotImplementedError()

    def note(self, message):
        """
        Formats a note admonition.

        :type message: str or list
        """
        raise NotImplementedError()

    def caution(self, message):
        """
        Formats a caution admonition.

        :type message: str or list
        """
        raise NotImplementedError()

    def table(self, headers, rows):
        """
        Formats a table.

        :type headers: list
        :type rows: list
        """
        raise NotImplementedError()

    def ask(self, question, default=None, validator=None):
        """
        Asks a question

        :type question: str
        :type default: str or None
        :type validator: callable or None

        :rtype: str
        """
        raise NotImplementedError()

    def ask_hidden(self, question, validator=None):
        """
        Asks a question with the user input hidden.

        :type question: str
        :type validator: callable or None

        :rtype: str
        """
        raise NotImplementedError()

    def confirm(self, question, default=True):
        """
        Asks for confirmation.

        :type question: str
        :type default: bool

        :rtype: bool
        """
        raise NotImplementedError()

    def choice(self, question, choices, default=None):
        """
        Asks a choice question.

        :type question: str
        :type choices: list
        :type default: str or int or None

        :rtype: str
        """
        raise NotImplementedError()

    def new_line(self, count=1):
        """
        Add newline(s).

        :param count: The number of newlines
        :type count: int
        """
        self._output.write(os.linesep * count)

    def create_progress_bar(self, max=0):
        """
        Create a new progress bar

        :type max: int

        :rtype ProgressHelper
        """
        return ProgressBar(self, max)

    def write(self, messages, newline=False, type=Output.OUTPUT_NORMAL):
        self._do_write(messages, newline, False, type)

    def write_error(self, messages, newline=False, type=Output.OUTPUT_NORMAL):
        self._do_write(messages, newline, True, type)

    def _do_write(self, messages, newline, stderr, type):
        if not isinstance(messages, list):
            messages = [messages]

        if stderr and isinstance(self._output, ConsoleOutput):
            self._output.get_error_output().write(messages, newline, type)
            self._last_message_err = '\n'.join(messages)

            return

        self._output.write(messages, newline, type)
        self._last_message = '\n'.join(messages)

    def writeln(self, messages, type=Output.OUTPUT_NORMAL):
        self.write(messages, True, type)

    def overwrite(self, messages, newline=False, size=None, type=Output.OUTPUT_NORMAL):
        self._do_overwrite(messages, newline, size, False, type)

    def _do_overwrite(self, messages, newline, size, stderr, type):
        # messages can be a list, let's convert it to string anyway
        if not isinstance(messages, list):
            messages = [messages]

        messages = '\n'.join(messages)

        # since overwrite is supposed to overwrite last message...
        if size is None:
            # removing possible formatting of lastMessage with strip_tags
            if stderr:
                message = self._last_message_err
            else:
                message = self._last_message

            size = Helper.len_without_decoration(self._output.get_formatter(), message)

        # ...let's fill its length with backspaces
        self._do_write('\x08' * size, False, stderr, type)

        # write the new message
        self._do_write(messages, False, stderr, type)

        fill = size - Helper.len_without_decoration(self._output.get_formatter(), messages)
        if fill > 0:
            # whitespace whatever has left
            self._do_write(' ' * fill, False, stderr, type)
            # move the cursor back
            self._do_write('\x08' * fill, False, stderr, type)

        if newline:
            self._do_write('', True, stderr, type)

        if stderr:
            self._last_message_err = messages
        else:
            self._last_message = messages

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
