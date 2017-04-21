# -*- coding: utf-8 -*-

import os
import copy
import textwrap
from .output_style import OutputStyle
from ..outputs import BufferedOutput
from ..helpers import Helper, Table, QuestionHelper
from ..questions import Question, ConfirmationQuestion, ChoiceQuestion
from ..formatters import Formatter


class CleoStyle(OutputStyle):

    MAX_LINE_LENGTH = 120

    def __init__(self, input, output):
        super(CleoStyle, self).__init__(output)

        self._input = input
        self._buffered_output = BufferedOutput(output.get_verbosity(), False, copy.deepcopy(output.get_formatter()))
        self._line_length = min(self._get_terminal_width(), self.MAX_LINE_LENGTH)

    def block(self, messages, type=None, style=None,
              prefix=' ', padding=False, type_style=None, indent_on_type=False):
        """
        Formats a message as a block of text.

        :param messages: The message to write in the block
        :type messages: str or list

        :param type: The block type (added in [] on first line)
        :type type: str or None

        :param style: The style to apply to the whole block
        :type style: str or None

        :param prefix: The prefix for the block
        :type prefix: str

        :param padding: Whether to add vertical padding
        :type padding: bool
        """
        self._auto_prepend_block()
        if not isinstance(messages, list):
            messages = [messages]

        lines = []

        # Add type
        if type is not None:
            messages[0] = '[%s] %s' % (type, messages[0])

            if indent_on_type:
                for key, message in enumerate(messages[1:]):
                    key = key + 1
                    messages[key] = ' ' * (Helper.len(type) + 1 + 2) + message

        # Wrap and add newlines for each element
        for key, message in enumerate(messages):
            message = Formatter.escape(message)
            wrap_limit = self._line_length - Helper.len(prefix)

            lines += os.linesep.join(textwrap.wrap(message, wrap_limit)).split(os.linesep)

            if messages and key < len(messages) - 1:
                lines.append('')

        if padding and self.is_decorated():
            lines.insert(0, '')
            lines.append('')

        new_lines = []
        for line in lines:
            line = '%s%s' % (prefix, line)
            line += ' ' * (self._line_length - Helper.len_without_decoration(self.get_formatter(), line))

            if style:
                line = '<%s>%s</>' % (style, line)

            new_lines.append(line)

        if type and type_style:
            n = 0 if not padding else 1
            split = new_lines[n].split('[%s]' % type)
            if len(split) > 1:
                new_lines[n] = split[0] + '[<%s>%s</>]' % (type_style, type) + split[1]
            else:
                new_lines[n] = '[<%s>%s</>]' % (type_style, type) + split[0]

        self.writeln(new_lines)
        self.new_line()

    def title(self, message):
        self._auto_prepend_block()
        self.writeln([
            '<comment>%s</>' % message,
            '<comment>%s</>' % ('=' * Helper.len_without_decoration(self.get_formatter(), message))
        ])

        self.new_line()

    def section(self, message):
        self._auto_prepend_block()
        self.writeln([
            '<comment>%s</>' % message,
            '<comment>%s</>' % ('-' * Helper.len_without_decoration(self.get_formatter(), message))
        ])

        self.new_line()

    def listing(self, elements):
        self._auto_prepend_text()
        elements = list(map(lambda element: ' * %s' % element, elements))

        self.writeln(elements)
        self.new_line()

    def comment(self, message):
        self._auto_prepend_text()

        if not isinstance(message, list):
            message = [message]

        for msg in message:
            self.writeln(' // %s' % msg)

    def success(self, message):
        self.block(message, 'OK', type_style='fg=green')

    def error(self, message):
        self.block(message, 'ERROR', 'fg=white;bg=red', padding=True)

    def warning(self, message):
        self.block(message, 'WARNING', type_style='fg=red')

    def note(self, message):
        self.block(message, 'NOTE', type_style='fg=blue')

    def caution(self, message):
        self.block(message, 'CAUTION', type_style='fg=red', indent_on_type=True)

    def table(self, headers, rows):
        headers = list(map(lambda header: '<info>%s</>' % header, headers))

        table = Table(self)
        table.set_headers(headers)
        table.set_rows(rows)

        table.render()
        self.new_line()

    def ask(self, question, default=None, validator=None):
        question = Question(question)
        question.validator = validator

        return self.ask_question(question)

    def ask_hidden(self, question, validator=None):
        question = Question(question)
        question.hidden = True
        question.validator = validator

        return self.ask_question(question)

    def confirm(self, question, default=True, true_answer_regex='(?i)^y'):
        return self.ask_question(
            ConfirmationQuestion(question, default, true_answer_regex)
        )

    def choice(self, question, choices, default=None):
        if default is not None:
            default = choices[default]

        return self.ask_question(ChoiceQuestion(question, choices, default))

    def ask_question(self, question):
        """
        Asks a question.

        :param question: The question to ask
        :type question: Question

        :rtype: str
        """
        if self._input.is_interactive():
            self._auto_prepend_block()

        answer = QuestionHelper().ask(self._input, self, question)

        if self._input.is_interactive():
            self.new_line()
            self._buffered_output.write('\n')

        return answer

    def writeln(self, messages, type=OutputStyle.OUTPUT_NORMAL):
        super(CleoStyle, self).writeln(messages, type)
        self._buffered_output.writeln(self._reduce_buffer(messages), type)

    def write(self, messages, newline=False, type=OutputStyle.OUTPUT_NORMAL):
        super(CleoStyle, self).write(messages, newline, type)
        self._buffered_output.write(self._reduce_buffer(messages), newline, type)

    def write_error(self, messages, newline=False, type=OutputStyle.OUTPUT_NORMAL):
        super(CleoStyle, self).write_error(messages, newline, type)
        self._buffered_output.write(self._reduce_buffer(messages), newline, type)

    def new_line(self, count=1):
        super(CleoStyle, self).new_line(count)
        self._buffered_output.write('\n' * count)

    def overwrite(self, messages, newline=False, size=None, type=OutputStyle.OUTPUT_NORMAL):
        super(CleoStyle, self).overwrite(messages, newline, size, type)
        self._buffered_output.write(self._reduce_buffer(messages), newline, type)

    def _get_terminal_width(self):
        from ..application import Application

        application = Application()
        width = application.terminal.width

        if width:
            return width

        return self.MAX_LINE_LENGTH

    def _auto_prepend_block(self):
        chars = self._buffered_output.fetch().replace(os.linesep, '\n')[:-2]

        if not chars:
            return self.new_line()

        # Prepend new line for each non LF chars (This means no blank line was output before)
        self.new_line(2 - chars.count('\n'))

    def _auto_prepend_text(self):
        fetched = self._buffered_output.fetch()

        # Prepend new line if last char isn't EOL:
        if fetched and fetched[-1] != '\n':
            self.new_line()

    def _reduce_buffer(self, messages):
        # We need to know if the two last chars are PHP_EOL
        # Preserve the last 4 chars inserted (PHP_EOL on windows is two chars) in the history buffer
        if not isinstance(messages, list):
            messages = [messages]

        return list(map(lambda m: m[:-4], [self._buffered_output.fetch()] + messages))
