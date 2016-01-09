# -*- coding: utf-8 -*-

from .output import Output


class BufferedOutput(Output):

    buffer = ''

    def fetch(self):
        """
        Empties buffer and returns its content.

        :rtype: str
        """
        content = self.buffer
        self.buffer = ''

        return content

    def do_write(self, message, newline):
        self.buffer += message

        if newline:
            self.buffer += '\n'
