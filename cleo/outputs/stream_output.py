# -*- coding: utf-8 -*-

import os
import platform
from io import UnsupportedOperation

from .output import Output
from .._compat import encode


class StreamOutput(Output):

    def __init__(self, stream, verbosity=Output.VERBOSITY_NORMAL, decorated=None, formatter=None):
        if not hasattr(stream, 'write') or not callable(stream.write):
            raise Exception('The StreamOutput class needs a stream '
                            'as its first argument.')

        self.stream = stream

        if decorated is None:
            decorated = self.has_color_support(decorated)

        super(StreamOutput, self).__init__(verbosity, decorated)

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
            message = encode(message)
            self.stream.write(message)

        self.stream.flush()

    def has_color_support(self, decorated):
        if platform.system().lower() == 'windows':
            return (
                os.getenv('ANSICON') is not None
                or 'ON' == os.getenv('ConEmuANSI')
                or 'xterm' == os.getenv('Term')
            )

        if not hasattr(self.stream, 'fileno'):
            return False

        try:
            return os.isatty(self.stream.fileno())
        except UnsupportedOperation:
            return False

    def flush(self):
        return self.stream.flush()
