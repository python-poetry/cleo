# -*- coding: utf-8 -*-

from pastel import Pastel


class Formatter(Pastel):

    def format(self, message):
        return self.colorize(message)

    def set_decorated(self, decorated):
        self.with_colors(decorated)

    def is_decorated(self):
        return self.is_colorized()
