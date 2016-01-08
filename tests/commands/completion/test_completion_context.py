# -*- coding: utf-8 -*-

from ... import CleoTestCase
from cleo.commands.completion.completion_context import CompletionContext


class CompletionContextTestCase(CleoTestCase):

    def test_word_break_split(self):
        context = CompletionContext()
        context.set_command_line('console  config:application --direction="west" --with-bruce --repeat 3')

        # Cursor at the end of the first word
        context.set_char_index(7)
        words = context.get_words()

        self.assertEqual(
            words,
            [
                'console',
                'config:application',
                '--direction',
                'west',
                '--with-bruce',
                '--repeat',
                '3'
            ]
        )
