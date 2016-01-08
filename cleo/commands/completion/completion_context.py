# -*- coding: utf-8 -*-

import re


class CompletionContext(object):
    """
    Command line context for completion
    """

    def __init__(self):
        self._command_line = ''
        self._char_index = 0
        self._words = None
        self._word_index = None
        self._word_breaks = "'\"()= \t\n"

    def set_command_line(self, command_line):
        self._command_line = command_line
        self._reset()

    def get_command_line(self):
        return self._command_line

    def set_char_index(self, index):
        self._char_index = index

    def get_current_word(self):
        if self.get_word_index() < len(self.get_words()):
            return self._words[self._word_index]

        return ''

    def get_word_at_index(self, index):
        if index < len(self.get_words()):
            return self._words[index]

        return ''

    def get_words(self):
        """
        :rtype: list
        """
        if self._words is None:
            self._split_command()

        return self._words

    def get_word_index(self):
        if self._word_index is None:
            self._split_command()

        return self._word_index

    def get_char_index(self):
        return self._char_index

    def set_word_breaks(self, word_breaks):
        self._word_breaks = word_breaks
        self._reset()

    def _split_command(self):
        self._words = []
        self._word_index = None
        cursor = 1

        breaks = re.escape(self._word_breaks)

        matches = re.findall('([^%s]*)([$%s]*)' % (breaks, breaks), self._command_line)
        if not matches:
            return

        # Groups:
        # 1: Word
        # 2: Break characters
        for index, match in enumerate(matches):
            # Determine which word the cursor is in
            whole_match = match[0] + match[1]
            cursor += len(whole_match)
            word = match[0]

            if self._word_index is None and cursor >= self._char_index:
                self._word_index = index

                # Find the cursor position relative to the end of the word
                cursor_word_offset = self._char_index - (cursor - len(match[1]) - 1)

                if cursor_word_offset < 0:
                    # Cursor is inside the word - truncate the word at the cursor
                    word = word[:len(word) + cursor_word_offset]
                elif cursor_word_offset > 0:
                    # Cursor is in the break-space after the word
                    # Push an empty word at the cursor
                    self._word_index += 1
                    self._words.append(word)
                    self._words.append('')

                    continue

            if word:
                self._words.append(word)

        if self._word_index > len(self._words) - 1:
            self._word_index = len(self._words) - 1

    def _reset(self):
        self._words = None
        self._word_index = None
