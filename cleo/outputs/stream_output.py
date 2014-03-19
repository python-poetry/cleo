# -*- coding: utf-8 -*-

import os
from io import UnsupportedOperation

from .output import Output


class StreamOutput(Output):

    def __init__(self, stream, verbosity=Output.VERBOSITY_NORMAL, decorated=None, formatter=None):
        if not hasattr(stream, 'write') or not callable(stream.write):
            raise Exception('The StreamOutput class needs a stream '
                            'as its first argument.')

        self.stream = stream

        if decorated is None:
            decorated = self.has_color_support(decorated)

        super(StreamOutput, self).__init__(verbosity, decorated, formatter)

    def get_stream(self):
        return self.stream

    def do_write(self, message, newline):
        message = (message + (os.linesep if newline else ''))

        # This try/catch block is a small hack
        # to handle the cases where the stream is a class
        # like BytesIO that accepts only bytes object
        try:
            self.stream.write(message)
        except TypeError:
            message = message.encode('utf-8')
            self.stream.write(message)

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
