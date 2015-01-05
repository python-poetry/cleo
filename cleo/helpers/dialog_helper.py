# -*- coding: utf-8 -*-

import sys
import os
import subprocess

from .helper import Helper
from ..formatters.output_formatter_style import OutputFormatterStyle
from ..validators import Choice, Callable, Validator, Integer, ValidationError


class DialogHelper(Helper):
    """
    The Dialog class provides helpers to interact with the user.
    """

    input_stream = None
    stty = None

    def select(self, output_, question, choices,
               default=None, attempts=False, error_message='Value "%s" is invalid'):
        """
        Asks the user to select a value.

        @param output_: An Output Instance
        @type output_: Output
        @param question: The question to ask
        @type question: str or list
        @param choices: List of choices to pick form
        @type choices: list
        @param default: The default answer if the user enters nothing
        @type default: mixed
        @param attempts: Max number of times to ask before giving up (false by default, which means infinite)
        @type attempts: bool or int
        @param error_message: Message which will be shown if invalid value from choice list would be picked
        @type error_message: str

        @return: The selected value (the key of the choices array)
        @rtype: integer or str
        """
        width = max(map(len, choices))

        if not isinstance(question, (list, tuple)):
            question = [question]

        messages = question
        for key, value in enumerate(choices):
            messages.append('  [<info>%-*s</info>] %s' % (width, key, value))

        output_.write(messages)

        def choose(picked):
            try:
                p = int(picked)
            except ValueError:
                raise Exception(error_message % picked)

            if p not in range(0, len(choices)):
                raise Exception(error_message % picked)

            return picked

        class SelectError(ValidationError):

            def to_s(self):
                return error_message % self.value

        class SelectChoice(Choice):

            def validate(self, choice):
                try:
                    return super(SelectChoice, self).validate(choice)
                except ValidationError as e:
                    self.error(choice)

            def error(self, choice):
                raise SelectError(error_message, choice)

        result = self.ask_and_validate(output_, '> ',
                                       SelectChoice(range(0, len(choices)), validator=Integer()),
                                       attempts, default)

        return result

    def ask(self, output_, question, default=None, autocomplete=None):
        """
        Asks a question to the user.

        @param output_: An Output Instance
        @type output_: Output
        @param question: The question to ask
        @type question: str or list
        @param default: The default answer if the user enters nothing
        @type default: mixed
        @param autocomplete: List of values to autocomplete
        @type autocomplete: list

        @return: The user answer
        @rtype: str
        """
        output_.write(question)

        input_stream = self.input_stream or sys.stdin

        if autocomplete is None or not self.has_stty_available():
            ret = input_stream.readline(4096).decode('utf-8')
            if not ret:
                raise Exception('Aborted')

            ret = ret.strip()
        else:
            ret = ''

            i = 0
            ofs = -1
            matches = autocomplete
            num_matches = len(matches)

            stty_mode = os.popen('stty -g')

            # Disable icanon (so we can fread each keypress) and echo (we'll do echoing here instead)
            os.popen('stty -icanon -echo')

            # Add highlighted text style
            output_.get_formatter().set_style('hl', OutputFormatterStyle('black', 'white'))

            # Read a keypress
            while True:
                c = input_stream.read(1)

                # Backspace character
                if c == '\177':
                    if num_matches == 0 and i != 0:
                        i -= 1
                        # Move cursor backwards
                        output_.write('\033[1D')

                    if i == 0:
                        ofs = -1
                        matches = autocomplete
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
                            output_.write(ret[:i])
                            i = len(ret)

                        if c == '\n':
                            output_.write(c)
                            break

                        num_matches = 0

                    continue
                else:
                    output_.write(c)
                    ret += c
                    i += 1

                    num_matches = 0
                    ofs = 0

                    for value in autocomplete:
                        # If typed characters match the beginning chunk of value (e.g. [AcmeDe]moBundle)
                        if value.startswith(ret):
                            num_matches += 1
                            matches[num_matches] = value

                # Erase characters from cursor to end of line
                output_.write('\033[K')

                if num_matches > 0 and ofs != -1:
                    # Save cursor position
                    output_.write('\0337')
                    # Write highlighted text
                    output_.write('<hl>' + matches[ofs][:i] + '</hl>')
                    # Restore cursor position
                    output_.write('\0338')

            os.popen('stty %s' % stty_mode)

        return ret if len(ret) > 0 else default

    def ask_confirmation(self, output_, question, default=True):
        """
        Asks a confirmation to the user.

        The question will be asked until the user answers by nothing, yes, or no.

        @param output_: An Output instance
        @type output_: Output
        @param question: The question to ask
        @type question: str or list
        @param default: The default answer if the user enters nothing
        @type default: mixed

        @return: True if the user has confirmed, False otherwise
        @rtype: bool
        """
        answer = 'z'
        while answer and str(answer[0]).lower() not in ['y', 'n']:
            answer = self.ask(output_, question)

        if default is False:
            return answer and answer[0].lower() == 'y'

        return not answer or answer[0].lower() == 'y'

    def ask_hidden_response(self, output_, question, fallback=True):
        """
        Asks a question to the user, the response is hidden

        @param output_: An Ouput instance
        @type output_: Output
        @param question: The question
        @type question: str
        @param fallback: Whether to fallback on non-hidden question or not
        @type fallback: bool

        @return: The answer
        @rtype: str
        """
        if self.has_stty_available():
            output_.write(question)

            stty_mode = subprocess.check_output(['stty', '-g'])

            subprocess.check_output(['stty', '-echo'])
            input_stream = self.input_stream or sys.stdin
            value = input_stream.readline(4096).decode('utf-8')
            subprocess.check_output(['stty', '%s' % stty_mode])

            if not value:
                raise Exception('Aborted')

            value = value.strip()
            output_.writeln('')

            return value

        if fallback:
            return self.ask(output_, question)

        raise Exception('Unable to hide the response')

    def ask_and_validate(self, output_, question, validator,
                         attempts=False, default=None, autocomplete=None):
        """
        Asks for a value and validates the response.

        The validator receives the data to validate. It must return the
        validated data when the data is valid and throw an exception
        otherwise.

        @param output_: An Output Instance
        @type output_: Output
        @param question: The question to ask
        @type question: str or list
        @param validator: A callback
        @type validator: callable or validator
        @param attempts: Max number of times to ask before giving up (false by default, which means infinite)
        @type attempts: bool or int
        @param default: The default answer if the user enters nothing
        @type default: mixed
        @param autocomplete: List of values to autocomplete
        @type autocomplete: list

        @rtype: mixed
        """
        def interviewer():
            return self.ask(output_, question, default, autocomplete)

        return self.validate_attempts(interviewer, output_, validator, attempts)

    def ask_hidden_response_and_validate(self, output_, question, validator,
                                         attempts=False, fallback=True):
        """
        Asks for a value, hide and validates the response.

        The validator receives the data to validate. It must return the
        validated data when the data is valid and throw an exception
        otherwise.

        @param output_: An Output Instance
        @type output_: Output
        @param question: The question to ask
        @type question: str or list
        @param validator: A callback
        @type validator: callable or Validator
        @param attempts: Max number of times to ask before giving up (false by default, which means infinite)
        @type attempts: bool or int
        @param fallback: Whether to fallback on non-hidden question or not
        @type fallback: bool

        @return: The answer
        @rtype: str
        """
        def interviewer():
            return self.ask_hidden_response(output_, question, fallback)

        return self.validate_attempts(interviewer, output_, validator, attempts)

    def set_input_stream(self, input_stream):
        """
        Sets the input stream to read from when interacting with the user.

        This is mainly useful for testing purpose.

        @param input_stream: The input stream
        """
        self.input_stream = input_stream

    def get_input_stream(self):
        """
        Returns the helper's input stream

        @return: The input stream
        @rtype: str
        """
        return self.input_stream

    def get_name(self):
        return 'dialog'

    def has_stty_available(self):
        if self.stty is not None:
            return self.stty

        exit_code = subprocess.call(['stty', '2'])
        self.stty = exit_code == 0

        return self.stty

    def validate_attempts(self, interviewer, output_, validator, attempts):
        """
        Validates an attempt

        @param interviewer: A callable that will ask for a question and return the result
        @type interviewer: callable
        @param output_: An Output Instance
        @type output_: Output
        @param validator: A callback
        @type validator: callable or Validator
        @param attempts: Max number of times to ask before giving up (false by default, which means infinite)
        @type attempts: bool or int

        @return: The validated response
        """
        error = None
        if not isinstance(validator, Validator):
            validator = Callable(validator)

        while attempts is False or attempts > 0:
            if attempts is not False:
                attempts -= 1

            if error is not None:
                output_.writeln(self.get_helper_set().get('formatter').format_block(str(error), 'error'))

            try:
                return validator.validate(interviewer())
            except Exception as e:
                error = e

        raise error
