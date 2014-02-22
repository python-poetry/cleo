# -*- coding: utf-8 -*-

import re

from .output_formatter_style import OutputFormatterStyle
from .output_formatter_style_stack import OutputFormatterStyleStack


class OutputFormatter(object):

    FORMAT_PATTERN = '(?is)(\\\\?)<(/?)([a-z][a-z0-9_=;-]+)?>((?:(?!\\\\?<).)*)'

    def __init__(self, decorated=False, styles=None):
        self.__decorated = bool(decorated)

        styles = styles or {}

        self.__styles = {}
        self.set_style('error', OutputFormatterStyle('white', 'red'))
        self.set_style('info', OutputFormatterStyle('green'))
        self.set_style('comment', OutputFormatterStyle('yellow'))
        self.set_style('question', OutputFormatterStyle('cyan'))

        for name, style in styles.items():
            self.set_style(name, style)

        self.__style_stack = OutputFormatterStyleStack()

    @classmethod
    def escape(cls, text):
        return re.sub('(?i)([^\\\\]?)<', '$1\\<', text)

    def set_decorated(self, decorated):
        self.__decorated = bool(decorated)

    def is_decorated(self):
        return self.__decorated

    def set_style(self, name, style):
        self.__styles[name] = style

    def has_style(self, name):
        return name in self.__styles

    def get_style(self, name):
        if self.has_style(name):
            return self.__styles[name]

    def format(self, message):
        message = re.sub(self.__class__.FORMAT_PATTERN, self.replace_style, message)

        return message.replace('\\<', '<')

    def replace_style(self, match):
        # we got "\<" escaped char
        if match.group(1) == '\\':
            return self.apply_current_style(match.group(0))

        if not match.group(3):
            if match.group(2) == '/':
                # we got "</>" tag
                self.__style_stack.pop()

                return self.apply_current_style(match.group(4))

            # we got "<>" tag
            return '<>' + self.apply_current_style(match.group(4))

        if match.group(3).lower() in self.__styles:
            style = self.__styles[match.group(3).lower()]
        else:
            style = self.create_style_from_string(match.group(3))

            if style is False:
                return self.apply_current_style(match.group(0))

        if match.group(2) == '/':
            self.__style_stack.pop(style)
        else:
            self.__style_stack.push(style)

        return self.apply_current_style(match.group(4))

    def create_style_from_string(self, string):
        matches = re.findall('([^=]+)=([^;]+)(;|$)', string.lower())
        if not len(matches):
            return False

        style = OutputFormatterStyle()

        for match in matches:
            if match[0] == 'fg':
                style.set_foreground(match[1])
            elif match[0] == 'bg':
                style.set_background(match[1])
            else:
                pass

        return style

    def apply_current_style(self, text):
        if self.is_decorated() and len(text):
            return self.__style_stack.get_current().apply(text)
        else:
            return text
