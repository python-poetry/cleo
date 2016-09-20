# -*- coding: utf-8 -*-

import re

from .output_formatter_style import OutputFormatterStyle
from .output_formatter_style_stack import OutputFormatterStyleStack


class OutputFormatter(object):

    FORMAT_PATTERN = '(?isx)(\\\\?)<(/?)([a-z][a-z0-9_=;-]*)?>((?: [^<\\\\]+ | (?!<(?:/?[a-z]|/>)). | .(?<=\\\\<) )*)'

    TAG_REGEX = '[a-z][a-z0-9_=;-]*'
    FULL_TAG_REGEX = re.compile('(?isx)<(({}) | /({})?)>'.format(TAG_REGEX, TAG_REGEX))

    def __init__(self, decorated=False, styles=None):
        self.__decorated = bool(decorated)

        styles = styles or {}

        self.__styles = {}
        self.set_style('error', OutputFormatterStyle('white', 'red'))
        self.set_style('info', OutputFormatterStyle('green'))
        self.set_style('comment', OutputFormatterStyle('yellow'))
        self.set_style('question', OutputFormatterStyle('black', 'cyan'))

        for name, style in styles.items():
            self.set_style(name, style)

        self.__style_stack = OutputFormatterStyleStack()

    @classmethod
    def escape(cls, text):
        return re.sub('(?is)([^\\\\]?)<', '\\1\\<', text)

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
        output = ''
        tags = []
        i = 0
        for m in self.FULL_TAG_REGEX.finditer(message):
            if i > 0:
                p = tags[i - 1]
                tags[i - 1] = (p[0], p[1], p[2], p[3], m.start(0))

            tags.append((m.group(0), m.end(0), m.group(1), m.group(3), None))

            i += 1

        if not tags:
            return message.replace('\\<', '<')

        offset = 0
        for t in tags:
            prev_offset = offset
            offset = t[1]
            endpos = t[4] if t[4] else -1
            text = t[0]
            if prev_offset < offset - len(text):
                output += self.apply_current_style(message[prev_offset:offset - len(text)])

            if offset != 0 and '\\' == message[offset - len(text) - 1]:
                output += self.apply_current_style(text)
                continue

            # opening tag?
            open = '/' != text[1]
            if open:
                tag = t[2]
            else:
                tag = t[3] if t[3] else ''

            style = self.create_style_from_string(tag.lower())
            if not open and not tag:
                # </>
                self.__style_stack.pop()
            elif style is False:
                output += self.apply_current_style(text)
            elif open:
                self.__style_stack.push(style)
            else:
                self.__style_stack.pop(style)

            # add the text up to the next tag
            output += self.apply_current_style(message[offset:endpos])
            offset += len(message[offset:endpos])

        output += self.apply_current_style(message[offset:])

        return output.replace('\\<', '<')

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
        if string in self.__styles:
            return self.__styles[string]

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
                try:
                    style.set_option(match[1])
                except ValueError:
                    return False

        return style

    def apply_current_style(self, text):
        if self.is_decorated() and len(text):
            return self.__style_stack.get_current().apply(text)
        else:
            return text
