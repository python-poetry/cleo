# -*- coding: utf-8 -*-

from .output_formatter_style import OutputFormatterStyle


class OutputFormatterStyleStack(object):

    def __init__(self, empty_style=None):
        self.empty_style = empty_style or OutputFormatterStyle()
        self.reset()

    def reset(self):
        self.styles = list()

    def push(self, style):
        self.styles.append(style)

    def pop(self, style=None):
        if not len(self.styles):
            return self.empty_style

        if not style:
            return self.styles.pop()

        for i, stacked_style in enumerate(reversed(self.styles)):
            if style.apply('') == stacked_style.apply(''):
                self.styles = self.styles[:len(self.styles) - 1 - i]

                return stacked_style

        raise Exception('Incorrectly nested style tag found.')

    def get_current(self):
        if not len(self.styles):
            return self.empty_style

        return self.styles[-1]
