# -*- coding: utf-8 -*-

import time
import re
import threading

from contextlib import contextmanager

from ..exceptions import CleoException
from ..outputs import Output
from .helper import Helper


class ProgressIndicator(object):

    formatters = None
    formats = {
        'normal': ' %indicator% %message%',
        'normal_no_ansi': ' %message%',

        'verbose': ' %indicator% %message% (%elapsed:6s%)',
        'verbose_no_ansi': ' %message% (%elapsed:6s%)',

        'very_verbose': ' %indicator% %message% (%elapsed:6s%)',
        'very_verbose_no_ansi': ' %message% (%elapsed:6s%)'
    }

    def __init__(self, output, fmt=None, indicator_change_interval=100, indicator_values=None):
        """
        Constructor.

        :param output: An Output instance
        :type output: Output

        :param fmt: Indicator format
        :type fmt: str or None

        :param indicator_change_interval: Change interval in milliseconds
        :type indicator_change_interval: int

        :param indicator_values: Animated indicator characters
        :type indicator_values: list or None
        """
        self._output = output

        if fmt is None:
            fmt = self._determine_best_format()

        if indicator_values is None:
            indicator_values = ['-', '\\', '|', '/']

        if len(indicator_values) < 2:
            raise CleoException('Must have at least 2 indicator value characters.')

        self.format = self.formats[fmt]
        self.indicator_change_interval = indicator_change_interval
        self.indicator_values = indicator_values

        self._message = None
        self._indicator_update_time = None
        self._started = False
        self._indicator_current = 0

        # Auto
        self._auto_running = None
        self._auto_thread = None

        self.start_time = time.time()

    def set_message(self, message):
        """
        Sets the current indicator message.

        :param message: The message
        :type message: str or None
        """
        self._message = message

        self._display()

    def get_message(self):
        return self._message

    @property
    def current_value(self):
        """
        Gets the current animated indicator character.

        :rtype: str
        """
        return self.indicator_values[self._indicator_current % len(self.indicator_values)]

    def start(self, message):
        """
        Starts the indicator output.

        :type message: str
        """
        if self._started:
            raise CleoException('Progress indicator already started.')

        self._message = message
        self._started = True
        self._last_message_length = 0
        self.start_time = time.time()
        self._indicator_update_time = self._get_current_time_in_milliseconds() + self.indicator_change_interval
        self._indicator_current = 0

        self._display()

    def advance(self):
        """
        Advance the indicator.
        """
        if not self._started:
            raise CleoException('Progress indicator has not yet been started.')

        if not self._output.is_decorated():
            return

        current_time = self._get_current_time_in_milliseconds()

        if current_time < self._indicator_update_time:
            return

        self._indicator_update_time = current_time + self.indicator_change_interval

        self._indicator_current += 1

        self._display()

    def finish(self, message, reset_indicator=False):
        """
        Finish the indicator with message.
        """
        if not self._started:
            raise CleoException('Progress indicator has not yet been started.')

        if self._auto_thread:
            self._auto_running.set()
            self._auto_thread.join()

        self._message = message

        if reset_indicator:
            self._indicator_current = 0

        self._display()
        self._output.writeln('')
        self._started = False

    @contextmanager
    def auto(self, start_message, end_message):
        """
        Auto progress. 
        """
        self._auto_running = threading.Event()
        self._auto_thread = threading.Thread(target=self._spin)

        self.start(start_message)
        self._auto_thread.start()

        try:
            yield self
        except (Exception, KeyboardInterrupt):
            self._output.writeln('')

            self._auto_running.set()
            self._auto_thread.join()

            raise

        self.finish(end_message, reset_indicator=True)

    def _spin(self):
        while not self._auto_running.is_set():
            self.advance()

            time.sleep(0.1)

    def _display(self):
        if self._output.get_verbosity() == Output.VERBOSITY_QUIET:
            return

        self._overwrite(re.sub('(?i)%([a-z\-_]+)(?:\:([^%]+))?%', self._overwrite_callback, self.format))

    def _overwrite_callback(self, matches):
        if hasattr(self, '_formatter_%s' % matches.group(1)):
            text = str(getattr(self, '_formatter_%s' % matches.group(1))())
        else:
            text = matches.group(0)

        return text

    def _overwrite(self, message):
        """
        Overwrites a previous message to the output.

        :param message: The message
        :type message: str
        """
        if self._output.is_decorated():
            self._output.write('\x0D\x1B[2K')
            self._output.write(message)
        else:
            self._output.writeln(message)

    def _determine_best_format(self):
        verbosity = self._output.get_verbosity()
        decorated = self._output.is_decorated()

        if verbosity == Output.VERBOSITY_VERBOSE:
            if decorated:
                return 'verbose'

            return 'verbose_no_ansi'
        elif verbosity in [Output.VERBOSITY_VERY_VERBOSE, Output.VERBOSITY_DEBUG]:
            if decorated:
                return 'very_verbose'

            return 'very_verbose_no_ansi'

        if decorated:
            return 'normal'

        return 'normal_no_ansi'

    def _get_current_time_in_milliseconds(self):
        return round(time.time() * 1000)

    def _formatter_indicator(self):
        return self.current_value

    def _formatter_message(self):
        return self.get_message()

    def _formatter_elapsed(self):
        return Helper.format_time(time.time() - self.start_time)
