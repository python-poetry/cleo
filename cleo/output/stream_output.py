# -*- coding: utf-8 -*-

import os
from io import UnsupportedOperation

from .output import Output


class StreamOutput(Output):

    def __init__(self, stream, verbosity=Output.VERBOSITY_NORMAL, decorated=None, formatter=None):
        self.stream = stream

        if decorated is None:
            decorated = self.has_color_support(decorated)

        super(StreamOutput, self).__init__(verbosity, decorated, formatter)

    def get_stream(self):
        return self.stream

    def do_write(self, message, newline):
        self.stream.write((message + (os.linesep if newline else '')).encode())
        self.stream.flush()

    def has_color_support(self, decorated):
        if os.pathsep == '\\':
            return os.getenv('ANSICON') is not None

        if not hasattr(self.stream, 'fileno'):
            return False

        try:
            return os.isatty(self.stream.fileno())
        except UnsupportedOperation:
            return False
