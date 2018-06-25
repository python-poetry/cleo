# -*- coding: utf-8 -*-

from ..formatters import Formatter


class OutputError(Exception):
    pass


class Output(object):

    VERBOSITY_QUIET = 16
    VERBOSITY_NORMAL = 32
    VERBOSITY_VERBOSE = 64
    VERBOSITY_VERY_VERBOSE = 128
    VERBOSITY_DEBUG = 256

    OUTPUT_NORMAL = 0
    OUTPUT_RAW = 1
    OUTPUT_PLAIN = 2

    def __init__(self, verbosity=VERBOSITY_NORMAL, decorated=False, formatter=None):
        self.verbosity = self.VERBOSITY_NORMAL if verbosity is None else verbosity
        self.formatter = formatter or Formatter(decorated)

    def set_formatter(self, formatter):
        self.formatter = formatter

    def get_formatter(self):
        return self.formatter

    def set_decorated(self, decorated):
        self.formatter.set_decorated(decorated)

    def is_decorated(self):
        return self.formatter.is_decorated()

    def set_verbosity(self, level):
        self.verbosity = int(level)

    def get_verbosity(self):
        return self.verbosity

    def is_quiet(self):
        return self.VERBOSITY_QUIET == self.verbosity

    def is_verbose(self):
        return self.VERBOSITY_VERBOSE <= self.verbosity

    def is_very_verbose(self):
        return self.VERBOSITY_VERY_VERBOSE <= self.verbosity

    def is_debug(self):
        return self.VERBOSITY_DEBUG <= self.verbosity

    def write(self, messages, newline=False, output_type=OUTPUT_NORMAL):
        if self.verbosity == self.VERBOSITY_QUIET:
            return

        if not isinstance(messages, (list, tuple)):
            messages = [messages]

        for message in messages:
            if output_type == self.OUTPUT_NORMAL:
                message = self.formatter.colorize(message)
            elif output_type == self.OUTPUT_RAW:
                pass
            elif output_type == self.OUTPUT_PLAIN:
                message = self.formatter.colorize(message)
            else:
                raise OutputError('Unknown output type given (%s)' % output_type)

            self.do_write(message, newline)

    def writeln(self, messages, output_type=OUTPUT_NORMAL):
        self.write(messages, True, output_type)

    def do_write(self, message, newline):
        raise NotImplementedError()
