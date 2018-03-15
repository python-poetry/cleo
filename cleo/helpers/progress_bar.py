# -*- coding: utf-8 -*-

from __future__ import division

import time
import re
import math
from ..outputs import Output, ConsoleOutput
from ..exceptions import CleoException
from .helper import Helper


class ProgressBar(object):
    """
    The ProgressBar provides helpers to display progress output.
    """

    # Options
    bar_width = 28
    bar_char = None
    empty_bar_char = '-'
    progress_char = '>'
    redraw_freq = 1

    formats = {
        'normal': ' %current%/%max% [%bar%] %percent:3s%%',
        'normal_nomax': ' %current% [%bar%]',

        'verbose': ' %current%/%max% [%bar%] %percent:3s%% %elapsed:-6s%',
        'verbose_nomax': ' %current% [%bar%] %elapsed:6s%',

        'very_verbose': ' %current%/%max% [%bar%] %percent:3s%% %elapsed:6s%/%estimated:-6s%',
        'very_verbose_nomax': ' %current% [%bar%] %elapsed:6s%',

        'debug': ' %current%/%max% [%bar%] %percent:3s%% %elapsed:6s%/%estimated:-6s%',
        'debug_nomax': ' %current% [%bar%] %elapsed:6s%'
    }

    def __init__(self, output, max=0):
        """
        Constructor.

        :param output: An Output instance
        :type output: Output

        :param max: Maximum steps (0 if unknown)
        :type max: int
        """
        if isinstance(output, ConsoleOutput):
            output = output.get_error_output()

        self._output = output
        self._max = 0
        self._step_width = None
        self._set_max_steps(max)
        self._step = 0
        self._percent = 0.0
        self._format = None
        self._internal_format = None
        self._format_line_count = 0
        self._last_messages_length = 0
        self._should_overwrite = True

        if not self._output.is_decorated():
            # Disable overwrite when output does not support ANSI codes.
            self._should_overwrite = False

            # Set a reasonable redraw frequency so output isn't flooded
            self.set_redraw_frequency(max / 10)

        self._messages = {}

        self._start_time = time.time()

    def set_message(self, message, name='message'):
        self._messages[name] = message

    def get_message(self, name='message'):
        return self._messages[name]

    def get_start_time(self):
        return self._start_time

    def get_max_steps(self):
        return self._max

    def get_progress(self):
        return self._step

    def get_progress_percent(self):
        return self._percent

    def set_bar_character(self, character):
        self.bar_char = character

        return self

    def get_bar_character(self):
        if self.bar_char is None:
            if self._max:
                return '='

            return self.empty_bar_char

        return self.bar_char

    def get_bar_width(self):
        return self.bar_width

    def set_bar_width(self, width):
        self.bar_width = width

        return self

    def get_empty_bar_character(self):
        return self.empty_bar_char

    def set_empty_bar_character(self, character):
        self.empty_bar_char = character

        return self

    def get_progress_character(self):
        return self.progress_char

    def set_progress_character(self, character):
        self.progress_char = character

        return self

    def set_format(self, fmt):
        self._format = None
        self._internal_format = fmt

    def set_redraw_frequency(self, freq):
        self.redraw_freq = max(freq, 1)

    def start(self, max=None):
        """
        Start the progress output.

        :param max: Number of steps to complete the bar (0 if indeterminate).
                    None to leave unchanged.
        :type max: int or None
        """
        self._start_time = time.time()
        self._step = 0
        self._percent = 0.0

        if max is not None:
            self._set_max_steps(max)

        self.display()

    def advance(self, step=1):
        """
        Advances the progress output X steps.

        :param step: Number of steps to advance.
        :type step: int
        """
        self.set_progress(self._step + step)

    def set_progress(self, step):
        """
        Sets the current progress.

        :param step: The current progress
        :type step: int
        """
        if self._max and step > self._max:
            self._max = step
        elif step < 0:
            step = 0

        prev_period = int(self._step / self.redraw_freq)
        curr_period = int(step / self.redraw_freq)

        self._step = step

        if self._max:
            self._percent = self._step / self._max
        else:
            self._percent = 0.0

        if prev_period != curr_period or self._max == step:
            self.display()

    def finish(self):
        """
        Finish the progress output.
        """
        if not self._max:
            self._max = self._step

        if self._step == self._max and not self._should_overwrite:
            return

        self.set_progress(self._max)

    def display(self):
        """
        Ouput the current progress string.
        """
        if self._output.get_verbosity() == Output.VERBOSITY_QUIET:
            return

        if self._format is None:
            self._set_real_format(self._internal_format or self._determine_best_format())

        self._overwrite(re.sub('(?i)%([a-z\-_]+)(?:\:([^%]+))?%', self._overwrite_callback, self._format))

    def _overwrite_callback(self, matches):
        if hasattr(self, '_formatter_%s' % matches.group(1)):
            text = str(getattr(self, '_formatter_%s' % matches.group(1))())
        elif matches.group(1) in self._messages:
            text = self._messages[matches.group(1)]
        else:
            return matches.group(0)

        if matches.group(2):
            if matches.group(2).startswith('-'):
                text = text.ljust(int(matches.group(2).lstrip('-').rstrip('s')))
            else:
                text = text.rjust(int(matches.group(2).rstrip('s')))

        return text

    def clear(self):
        """
        Removes the progress bar from the current line.

        This is useful if you wish to write some output
        while a progress bar is running.
        Call display() to show the progress bar again.
        """
        if not self._should_overwrite:
            return

        if self._format is None:
            self._set_real_format(self._internal_format or self._determine_best_format())

        self._overwrite('\n' * self._format_line_count)

    def _set_real_format(self, fmt):
        """
        Sets the progress bar format.
        """
        # try to use the _nomax variant if available
        if not self._max and fmt + '_nomax' in self.formats:
            self._format = self.formats[fmt + '_nomax']
        elif fmt in self.formats:
            self._format = self.formats[fmt]
        else:
            self._format = fmt

        self._format_line_count = self._format.count('\n')

    def _set_max_steps(self, mx):
        """
        Sets the progress bar maximal steps.

        :type mx: int
        """
        self._max = max(0, mx)

        if self._max:
            self._step_width = Helper.len(str(self._max))
        else:
            self._step_width = 4

    def _overwrite(self, message):
        """
        Overwrites a previous message to the output.

        :type message: str
        """
        lines = message.split('\n')

        # Append whitespace to match the line's length
        if self._last_messages_length is not None:
            for i, line in enumerate(lines):
                if self._last_messages_length > Helper.len_without_decoration(self._output.get_formatter(), line):
                    lines[i] = line.ljust(self._last_messages_length, '\x20')

        if self._should_overwrite:
            # move back to the beginning of the progress bar before redrawing it
            self._output.write('\x0D')
        elif self._step > 0:
            # move to new line
            self._output.writeln('')

        if self._format_line_count:
            self._output.write('\033[%dA' % self._format_line_count)

        self._output.write('\n'.join(lines))

        self._last_messages_length = 0

        for line in lines:
            length = Helper.len_without_decoration(self._output.get_formatter(), line)
            if length > self._last_messages_length:
                self._last_messages_length = length

    def _determine_best_format(self):
        verbosity = self._output.get_verbosity()

        if verbosity == Output.VERBOSITY_VERBOSE:
            if self._max:
                return 'verbose'

            return 'verbose_nomax'
        elif verbosity == Output.VERBOSITY_VERY_VERBOSE:
            if self._max:
                return 'very_verbose'

            return 'very_verbose_nomax'
        elif verbosity == Output.VERBOSITY_DEBUG:
            if self._max:
                return 'debug'

            return 'debug_nomax'

        if self._max:
            return 'normal'

        return 'normal_nomax'

    def _formatter_bar(self):
        if self._max:
            complete_bars = math.floor(self._percent * self.bar_width)
        else:
            complete_bars = math.floor(self.get_progress() % self.bar_width)

        display = self.get_bar_character() * int(complete_bars)

        if complete_bars < self.bar_width:
            empty_bars = (
                self.bar_width
                - complete_bars
                - Helper.len_without_decoration(self._output.get_formatter(), self.progress_char)
            )
            display += self.progress_char + self.empty_bar_char * int(empty_bars)

        return display

    def _formatter_elapsed(self):
        return Helper.format_time(time.time() - self._start_time)

    def _formatter_remaining(self):
        if not self._max:
            raise CleoException(
                'Unable to display the remaining time '
                'if the maximum number of steps is not set.'
            )

        if not self._step:
            remaining = 0
        else:
            remaining = (
                round(
                    (time.time() - self._start_time) / self._step
                    * (self._max - self._max)
                )
            )

        return Helper.format_time(remaining)

    def _formatter_estimated(self):
        if not self._max:
            raise CleoException(
                'Unable to display the estimated time '
                'if the maximum number of steps is not set.'
            )

        if not self._step:
            estimated = 0
        else:
            estimated = (
                round(
                    (time.time() - self._start_time) / self._step
                    * self._max
                )
            )

        return estimated

    def _formatter_current(self):
        return str(self._step).rjust(self._step_width, ' ')

    def _formatter_max(self):
        return self._max

    def _formatter_percent(self):
        return int(math.floor(self._percent * 100))
