# -*- coding: utf-8 -*-

from .output import Output
from ..formatter import OutputFormatter


class NullOutput(Output):

    def set_formatter(self, formatter):
        pass

    def get_formatter(self):
        return OutputFormatter()

    def set_decorated(self, decorated):
        pass

    def is_decorated(self):
        return False

    def set_verbosity(self, level):
        pass

    def get_verbosity(self):
        return self.VERBOSITY_QUIET

    def writeln(self, messages, output_type=Output.OUTPUT_NORMAL):
        pass

    def write(self, messages,
              newline=False,
              output_type=Output.OUTPUT_NORMAL):
        pass
