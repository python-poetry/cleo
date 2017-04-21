# -*- coding: utf-8 -*-

import sys
from .stream_output import StreamOutput


class ConsoleOutput(StreamOutput):

    def __init__(self, verbosity=StreamOutput.VERBOSITY_NORMAL,
                 decorated=None, formatter=None):
        output_stream = sys.stdout

        super(ConsoleOutput, self).__init__(output_stream,
                                            verbosity, decorated)

        self.stderr = StreamOutput(sys.stderr,
                                   verbosity, decorated, formatter)

    def set_decorated(self, decorated):
        super(ConsoleOutput, self).set_decorated(decorated)
        self.stderr.set_decorated(decorated)

    def set_formatter(self, formatter):
        super(ConsoleOutput, self).set_formatter(formatter)
        self.stderr.set_formatter(formatter)

    def set_verbosity(self, level):
        super(ConsoleOutput, self).set_verbosity(level)
        self.stderr.set_verbosity(level)

    def get_error_output(self):
        return self.stderr

    def set_error_output(self, error):
        self.stderr = error
