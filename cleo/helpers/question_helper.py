# -*- coding: utf-8 -*-

import sys
import os
import subprocess
import getpass

from .helper import Helper
from ..questions import Question, ChoiceQuestion, ConfirmationQuestion
from ..outputs import ConsoleOutput
from ..formatters import Formatter
from ..validators import Validator, Callable
from .._compat import decode


class QuestionHelper(Helper):

    name = 'question'

    _input_stream = None
    stty = None

    def ask(self, input_, output, question):
        """
        Asks a question to the user.

        :param input_: An Input instance
        :type input_: Input

        :param output: An Output instance
        :type output: Output

        :param question: The question to ask
        :type question: Question

        :return: The user answer
        :rtype: str
        """
        if isinstance(output, ConsoleOutput):
            output = output.get_error_output()

        if not input_.is_interactive():
            return question.default

        if not self._input_stream:
            self._input_stream = input_.get_stream()

        if not question.validator:
            return self._do_ask(output, question)

        interviewer = lambda: self._do_ask(output, question)

        return self._validate_attempts(interviewer, output, question)

    @property
    def input_stream(self):
        return self._input_stream or sys.stdin

    @input_stream.setter
    def input_stream(self, stream):
        self._input_stream = stream

    def _do_ask(self, output, question):
        """
        Asks a question to the user.

        :param output: An Output instance
        :type output: Output

        :param question: The question to ask
        :type question: Question

        :rtype: mixed
        """
        self._write_prompt(output, question)

        input_stream = self.input_stream
        autocomplete = question.autocompleter_values

        if autocomplete is None or not self._has_stty_available():
            ret = False

            if question.hidden:
                try:
                    ret = self._get_hidden_response(output, input_stream)
                except RuntimeError:
                    if not question.hidden_fallback:
                        raise

            if not ret:
                ret = self._read_from_input(input_stream)
        else:
            ret = self._autocomplete(output, question, input_stream)

        if len(ret) <= 0:
            ret = question.default

        if question.normalizer:
            return question.normalizer(ret)

        return ret

    def _write_prompt(self, output, question):
        """
        Outputs the question prompt.

        :param output: An Output instance
        :type output: Output

        :param question: The question to ask
        :type question: Question
        """
        message = question.question
        default = question.default

        if default is None:
            if isinstance(question, ChoiceQuestion):
                message = '<question>{}</>: '.format(message)
            else:
                message = '<question>{}</> '.format(message)
        elif isinstance(question, ConfirmationQuestion):
            message = '<question>{} (yes/no)</> [<comment>{}</>] '.format(
                message,
                'yes' if default else 'no'
            )
        elif isinstance(question, ChoiceQuestion) and question.multiselect:
            choices = question.choices
            default = default.split(',')

            for i, value in enumerate(default):
                default[i] = choices[int(value.strip())]

            message = '<question>{}</> [<comment>{}</>]:'.format(
                message,
                Formatter.escape(', '.join(default))
            )
        elif isinstance(question, ChoiceQuestion):
            choices = question.choices
            message = '<question>{}</question> [<comment>{}</>]:'.format(
                message,
                Formatter.escape(choices[int(default)])
            )

        if isinstance(question, ChoiceQuestion):
            if len(question.choices) > 1:
                width = max(*map(self.len, [str(k) for k, _ in enumerate(question.choices)]))
            else:
                width = self.len('0')

            messages = [message]
            for key, value in enumerate(question.choices):
                messages.append(' [<comment>{:{}}</>] {}'.format(key, width, value))

            output.writeln(messages)

            message = question.prompt

        output.write(message)

    def _write_error(self, output, error):
        """
        Outputs an error message.

        :param output: An Output instance
        :type output: Output

        :param error: A Exception instance
        :type error: Exception
        """
        if self.helper_set is not None and self.helper_set.has('formatter'):
            message = self.helper_set.get('formatter').format_block(decode(str(error)), 'error')
        else:
            message = '<error>%s</error>' % decode(str(error))

        output.writeln(message)

    def _autocomplete(self, output, question, input_stream):
        """
        Autocomplete a question.

        :param output: An Output instance
        :type output: Output

        :param question: The question to ask
        :type question: Question

        :rtype: str
        """
        autocomplete = question.autocompleter_values

        ret = ''

        i = 0
        ofs = -1
        matches = [x for x in autocomplete]
        num_matches = len(matches)

        stty_mode = decode(subprocess.check_output(['stty', '-g'])).rstrip('\n')

        # Disable icanon (so we can fread each keypress) and echo (we'll do echoing here instead)
        subprocess.check_output(['stty', '-icanon', '-echo'])

        # Add highlighted text style
        output.get_formatter().add_style('hl', 'black', 'white')

        # Read a keypress
        while True:
            c = input_stream.read(1)

            # Backspace character
            if c == '\177':
                if num_matches == 0 and i != 0:
                    i -= 1
                    # Move cursor backwards
                    output.write('\033[1D')

                if i == 0:
                    ofs = -1
                    matches = [x for x in autocomplete]
                    num_matches = len(matches)
                else:
                    num_matches = 0

                # Pop the last character off the end of our string
                ret = ret[:i]
            # Did we read an escape sequence
            elif c == '\033':
                c += input_stream.read(2)

                # A = Up Arrow. B = Down Arrow
                if c[2] == 'A' or c[2] == 'B':
                    if c[2] == 'A' and ofs == -1:
                        ofs = 0

                    if num_matches == 0:
                        continue

                    ofs += -1 if c[2] == 'A' else 1
                    ofs = (num_matches + ofs) % num_matches
            elif ord(c) < 32:
                if c == '\t' or c == '\n':
                    if num_matches > 0 and ofs != -1:
                        ret = matches[ofs]
                        # Echo out remaining chars for current match
                        output.write(ret[i:])
                        i = len(ret)

                    if c == '\n':
                        output.write(c)
                        break

                    num_matches = 0

                continue
            else:
                output.write(c)
                ret += c
                i += 1

                num_matches = 0
                ofs = 0

                for value in autocomplete:
                    # If typed characters match the beginning chunk of value (e.g. [AcmeDe]moBundle)
                    if value.startswith(ret) and i != len(value):
                        num_matches += 1
                        matches[num_matches - 1] = value

            # Erase characters from cursor to end of line
            output.write('\033[K')

            if num_matches > 0 and ofs != -1:
                # Save cursor position
                output.write('\0337')
                # Write highlighted text
                output.write('<hl>' + matches[ofs][i:] + '</hl>')
                # Restore cursor position
                output.write('\0338')

        subprocess.call(['stty', '%s' % decode(stty_mode)])

        return ret

    def _get_hidden_response(self, output, input_stream):
        """
        Gets a hidden response from user.

        :param output: An Output instance
        :type output: Output

        :rtype: str
        """
        if hasattr(output, 'output'):
            output = output.output

        return getpass.getpass('', stream=output)

    def _validate_attempts(self, interviewer, output, question):
        """
        Validates an attempt.

        :param interviewer: A callable that will ask for a question and return the result
        :type interviewer: callable

        :param output: An Output instance
        :type output: Output

        :param question: The question to ask
        :type question: Question

        :return: The validate response
        :rtype: str
        """
        error = None
        attempts = question.max_attempts

        if not isinstance(question.validator, Validator):
            validator = Callable(question.validator)
        else:
            validator = question.validator

        while attempts is None or attempts:
            if error is not None:
                self._write_error(output, error)

            try:
                return validator.validate(interviewer())
            except Exception as e:
                error = e

            if attempts is not None:
                attempts -= 1

        raise error

    def _read_from_input(self, stream):
        """
        Read user input.

        :param stream: The input stream

        :return:
        """
        if stream == sys.stdin:
            ret = stream.readline()
        else:
            ret = stream.readline(4096)

        if not ret:
            raise RuntimeError('Aborted')

        return decode(ret.strip())

    def _has_stty_available(self):
        if self.stty is not None:
            return self.stty

        devnull = open(os.devnull, 'w')

        try:
            exit_code = subprocess.call(['stty'], stdout=devnull, stderr=devnull)
        except Exception:
            exit_code = 2

        self.stty = exit_code == 0

        return self.stty

    def get_name(self):
        return self.name
