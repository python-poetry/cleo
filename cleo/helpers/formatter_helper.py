# -*- coding: utf-8 -*-

from .helper import Helper
from ..formatters import Formatter


class FormatterHelper(Helper):

    name = 'formatter'

    def format_section(self, section, message, style='info'):
        return '<%s>[%s]</%s> %s' % (style, section, style, message)

    def format_block(self, messages, style, large=False):
        messages = [messages] if not isinstance(messages, (list, tuple)) else messages

        l = 0
        lines = []
        for message in messages:
            message = Formatter.escape(message)
            lines.append(('  %s  ' if large else ' %s ') % message)
            l = max(len(message) + (4 if large else 2), l)

        messages = [' ' * l] if large else []
        for line in lines:
            messages.append(line + ' ' * (l - len(line)))

        if large:
            messages.append(' ' * l)

        messages = map(lambda m: '<%s>%s</%s>' % (style, m, style), messages)

        return '\n'.join(messages)

    def get_name(self):
        return 'formatter'
