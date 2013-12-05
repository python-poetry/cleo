# -*- coding: utf-8 -*-

from ..formatter.output_formatter import OutputFormatter


class OutputError(Exception):
    pass


class Output(object):

    VERBOSITY_QUIET = 0
    VERBOSITY_NORMAL = 1
    VERBOSITY_VERBOSE = 2

    OUTPUT_NORMAL = 0
    OUTPUT_RAW = 1
    OUTPUT_PLAIN = 2

    def __init__(self, verbosity=VERBOSITY_NORMAL, decorated=None, formatter=None):
        self.verbosity = verbosity or self.__class__.VERBOSITY_NORMAL
        self.formatter = formatter or OutputFormatter()
        self.formatter.set_decorated(bool(decorated))

    def set_formatter(self, formatter):
        self.formatter = formatter

    def get_formatter(self):
        return self.formatter

    def set_decorated(self, decorated):
        self.formatter.set_decorated(bool(decorated))

    def is_decorated(self):
        return self.formatter.is_decorated()

    def set_verbosity(self, level):
        self.verbosity = int(level)

    def get_verbosity(self):
        return self.verbosity

    def write(self, messages, newline=False, output_type=OUTPUT_NORMAL):
        if self.verbosity == self.__class__.VERBOSITY_QUIET:
            return

        if not isinstance(messages, (list, tuple)):
            messages = [messages]

        for message in messages:
            if output_type == self.__class__.OUTPUT_NORMAL:
                message = self.formatter.format(message)
            elif output_type == self.__class__.OUTPUT_RAW:
                pass
            elif output_type == self.__class__.OUTPUT_PLAIN:
                message = self.formatter.format(message)
            else:
                raise OutputError('Unknown output type given (%s)' % output_type)

            self.do_write(message, newline)

    def writeln(self, messages, output_type=OUTPUT_NORMAL):
        self.write(messages, True, output_type)

    def do_write(self, message, newline):
        raise NotImplementedError()