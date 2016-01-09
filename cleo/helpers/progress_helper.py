# -*- coding: utf-8 -*-

import time
import math
import warnings

from .helper import Helper
from ..outputs.output import Output


class ProgressHelper(Helper):
    """
    The Progress class providers helpers to display progress output.
    """

    FORMAT_QUIET = ' %percent%%'
    FORMAT_NORMAL = ' %current%/%max% [%bar%] %percent%%'
    FORMAT_VERBOSE = ' %current%/%max% [%bar%] %percent% Elapsed: %elapsed%'
    FORMAT_QUIET_NOMAX = ' %current%'
    FORMAT_NORMAL_NOMAX = ' %current% [%bar%]'
    FORMAT_VERBOSE_NOMAX = ' %current% [%bar%] Elapsed: %elapsed%'

    # options
    bar_width = 28
    bar_char = '='
    empty_bar_char = '-'
    progress_char = '>'
    display_format = None
    redraw_freq = 1

    last_messages_length = None
    bar_char_original = None

    output = None
    current_step = 0
    max_steps = 0
    start_time = None

    default_format_vars = [
        'current',
        'max',
        'bar',
        'percent',
        'elapsed'
    ]

    format_vars = []

    widths = {
        'current': 4,
        'max': 4,
        'percent': 3,
        'elapsed': 6
    }

    time_formats = [
        (0, '???'),
        (2, '1 sec'),
        (59, 'secs', 1),
        (60, '1 min'),
        (3600, 'mins', 60),
        (5400, '1 hr'),
        (86400, 'hrs', 3600),
        (129600, '1 day'),
        (604800, 'days', 86400)
    ]

    def __init__(self):
        warnings.warn('ProgressHelper class is deprecated. '
                      'Use the ProgressBar class instead', DeprecationWarning)

    def set_bar_width(self, size):
        """
        Sets the progress bar with

        :param size: The progress bar size
        :type size: int
        """
        self.bar_width = size

    def set_bar_character(self, char):
        """
        Sets the progress bar character

        :param char: The progress bar character
        :type char: str
        """
        self.bar_char = char

    def set_empty_bar_character(self, char):
        """
        Sets the empty bar character

        :param char: A character
        :type char: str
        """
        self.empty_bar_char = char

    def set_progress_character(self, char):
        """
        Sets the progress character

        :param char: A character
        :type char: str
        """
        self.progress_char = char

    def set_display_format(self, display_format):
        """
        Sets the progress bar format

        :param display_format: The display format
        :type display_format: str
        """
        self.display_format = display_format

    def set_redraw_frequency(self, freq):
        """
        Sets the redraw frequency

        :param freq: The redraw frequency in seconds
        :type freq: int
        """
        self.redraw_freq = freq

    def start(self, output_, max_steps=None):
        """
        Starts the progress output

        :param output_: An Output instance
        :type output_: Output
        :param max_steps: Maximum steps
        :type max_steps: int
        """
        self.start_time = time.time()
        self.current_step = 0
        self.max_steps = int(max_steps or 0)
        self.output = output_

        if self.display_format is None:
            if self.output.get_verbosity() == Output.VERBOSITY_QUIET:
                self.display_format = self.FORMAT_QUIET_NOMAX
                if self.max_steps > 0:
                    self.display_format = self.FORMAT_QUIET
            elif self.output.get_verbosity() == Output.VERBOSITY_VERBOSE:
                self.display_format = self.FORMAT_VERBOSE_NOMAX
                if self.max_steps > 0:
                    self.display_format = self.FORMAT_VERBOSE
            else:
                self.display_format = self.FORMAT_NORMAL_NOMAX
                if self.max_steps > 0:
                    self.display_format = self.FORMAT_NORMAL

        self.initialize()

    def advance(self, step=1, redraw=False):
        """
        Advances the progress output X steps

        :param step: Number of steps to advance
        :type step: int
        :param redraw: Whether to redraw or not
        :type redraw: bool
        """
        if self.start_time is None:
            raise Exception('You must start the progress bar before calling advance().')

        if self.current_step == 0:
            redraw = True

        self.current_step += step
        if redraw or self.current_step % self.redraw_freq == 0:
            self.display()

    def display(self, finish=False):
        """
        Ouputs the current progress string

        :param finish: Forces the end result
        :type finish: bool
        """
        if self.start_time is None:
            raise Exception('You must start the progress bar before calling display().')

        message = self.display_format
        for name, value in self.generate(finish).items():
            message = message.replace('%' + name + '%', str(value))

        self.overwrite(self.output, message)

    def finish(self):
        """
        Finishes the progress output
        """
        if self.start_time is None:
            raise Exception('You must start the progress bar before calling finish().')

        if not self.max_steps:
            self.bar_char = self.bar_char_original
            self.display(True)
        else:
            if self.current_step < self.max_steps:
                self.advance(self.max_steps - self.current_step)

        self.start_time = None
        self.output.writeln('')
        self.output = None

    def initialize(self):
        """
        Initializes the progress output
        """
        self.format_vars = []
        for v in self.default_format_vars:
            if self.display_format.find('%' + v + '%') != -1:
                self.format_vars.append(v)

        if self.max_steps > 0:
            self.widths['max'] = len(str(self.max_steps))
            self.widths['current'] = self.widths['max']
        else:
            self.bar_char_original = self.bar_char
            self.bar_char = self.empty_bar_char

    def generate(self, finish=False):
        """
        Generates the array map of format variables to values.

        :param finish: Forces the end result
        :type finish: bool

        :return: A dict of format vars and values
        :rtype: dict
        """
        format_vars = {}
        percent = 0
        if self.max_steps > 0:
            percent = round(float(self.current_step) / self.max_steps, 2)

        # bar
        if 'bar' in self.format_vars:
            if self.max_steps > 0:
                complete_bars = math.floor(percent * self.bar_width)
            else:
                if not finish:
                    complete_bars = math.floor(self.current_step % self.bar_width)
                else:
                    complete_bars = self.bar_width

            empty_bars = self.bar_width - complete_bars - len(self.progress_char)
            bar = self.bar_char * int(complete_bars)
            if complete_bars < self.bar_width:
                bar += self.progress_char
                bar += self.empty_bar_char * int(empty_bars)

            format_vars['bar'] = bar

        # elapsed
        if 'elapsed' in self.format_vars:
            elapsed = time.time() - self.start_time
            format_vars['elapsed'] = self.humane_time(elapsed).rjust(self.widths['elapsed'], ' ')

        # current
        if 'current' in self.format_vars:
            format_vars['current'] = str(self.current_step).rjust(self.widths['current'], ' ')

        # max steps
        if 'max' in self.format_vars:
            format_vars['max'] = self.max_steps

        # percent
        if 'percent' in self.format_vars:
            format_vars['percent'] = str(int(round(percent * 100))).rjust(self.widths['percent'], ' ')

        return format_vars

    def humane_time(self, secs):
        """
        Converts seconds into human-readable format

        :param secs: Number of seconds
        :type secs: int

        :return: Time in human-readable format
        :rtype: str
        """
        text = ''
        for time_format in self.time_formats:
            if secs < time_format[0]:
                if len(time_format) == 2:
                    text = time_format[1]
                    break
                else:
                    text = str(int(math.ceil(secs / time_format[2]))) + ' ' + time_format[1]
                    break

        return text

    def overwrite(self, output_, messages):
        """
        Overwrites a previous message to the output.

        :param output_: An Output instance
        :type output_: Output
        :param messages: The message as an array of lines or a single string
        :type messages: list or str
        """
        length = len(messages)

        # append whitespace to match the last line's length
        if self.last_messages_length is not None and self.last_messages_length > length:
            messages = messages.ljust(self.last_messages_length, '\x20')

        # carriage return
        output_.write('\x0D')
        output_.write(messages)

        self.last_messages_length = len(messages)

    def get_name(self):
        return 'progress'
