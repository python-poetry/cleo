# -*- coding: utf-8 -*-

try:
    from collections import OrderedDict
except ImportError:
    # python 2.6 or earlier, use backport
    from ordereddict import OrderedDict


class OutputFormatterStyle(object):

    FOREGROUND_COLORS = {
        'black': 30,
        'red': 31,
        'green': 32,
        'yellow': 33,
        'blue': 34,
        'magenta': 35,
        'cyan': 36,
        'white': 37
    }

    BACKGROUND_COLORS = {
        'black': 40,
        'red': 41,
        'green': 42,
        'yellow': 43,
        'blue': 44,
        'magenta': 45,
        'cyan': 46,
        'white': 47
    }

    OPTIONS = {
        'bold': 1,
        'underscore': 4,
        'blink': 5,
        'reverse': 7,
        'conceal': 8,
    }

    def __init__(self, foreground=None, background=None, options=None):
        self.foreground = None
        self.background = None

        if foreground:
            self.set_foreground(foreground)

        if background:
            self.set_background(background)

        options = options or []
        if not isinstance(options, list):
            options = [options]

        self.set_options(options)

    def set_foreground(self, foreground):
        self.foreground = self.FOREGROUND_COLORS[foreground]

    def set_background(self, background):
        self.background = self.BACKGROUND_COLORS[background]

    def set_option(self, option):
        if option not in self.OPTIONS:
            raise ValueError('Invalid option specified: "%s". Expected one of (%s)'
                             % (option, ', '.join(self.OPTIONS.keys())))

        if option not in self.options:
            self.options[self.OPTIONS[option]] = option

    def unset_option(self, option):
        if not option in self.OPTIONS:
            raise ValueError('Invalid option specified: "%s". Expected one of (%s)'
                             % (option, ', '.join(self.OPTIONS.keys())))

        del self.options[self.OPTIONS[option]]

    def set_options(self, options):
        self.options = OrderedDict()

        for option in options:
            self.set_option(option)

    def apply(self, text):
        codes = []

        if self.foreground:
            codes.append(self.foreground)

        if self.background:
            codes.append(self.background)

        if len(self.options):
            codes += list(self.options.keys())

        if not len(codes):
            return text

        return '\033[%sm%s\033[0m' % (';'.join(map(str, codes)), text)
