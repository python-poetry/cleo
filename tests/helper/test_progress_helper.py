# -*- coding: utf-8 -*-

import StringIO

from unittest import TestCase
from cleo.helper.progress_helper import ProgressHelper
from cleo.output.stream_output import StreamOutput


class ProgressHelperTest(TestCase):

    last_messages_length = None

    def test_advance(self):
        """
        ProgressHelper.advance() behaves properly
        """
        progress = ProgressHelper()
        output = self.get_output_stream()
        progress.start(output)
        progress.advance()

        output.get_stream().seek(0)
        self.assertEqual(self.generate_output('    1 [->--------------------------]'),
                         output.get_stream().read())

    def test_advance_with_steps(self):
        """
        ProgressHelper.advance() behaves properly with steps
        """
        progress = ProgressHelper()
        output = self.get_output_stream()
        progress.start(output)
        progress.advance(5)

        output.get_stream().seek(0)
        self.assertEqual(self.generate_output('    5 [----->----------------------]'),
                         output.get_stream().read())

    def test_advance_multiple_times(self):
        """
        ProgressHelper.advance() behaves properly when advancing multiple times
        """
        progress = ProgressHelper()
        output = self.get_output_stream()
        progress.start(output)
        progress.advance(3)
        progress.advance(2)

        output.get_stream().seek(0)
        self.assertEqual(self.generate_output('    3 [--->------------------------]')
                         + self.generate_output('    5 [----->----------------------]'),
                         output.get_stream().read())

    def test_customizations(self):
        """
        Customizing ProgressHelper should be possible
        """
        progress = ProgressHelper()
        progress.set_bar_width(10)
        progress.set_bar_character('_')
        progress.set_empty_bar_character(' ')
        progress.set_progress_character('/')
        progress.set_display_format(' %current%/%max% [%bar%] %percent%%')

        output = self.get_output_stream()
        progress.start(output, 10)
        progress.advance()

        output.get_stream().seek(0)
        self.assertEqual(self.generate_output('  1/10 [_/        ]  10%'),
                         output.get_stream().read())

    def test_percent(self):
        """
        Percentage should behave properly for ProgressHelper
        """
        progress = ProgressHelper()
        output = self.get_output_stream()
        progress.start(output, 50)
        progress.display()
        progress.advance()
        progress.advance()

        output.get_stream().seek(0)
        self.assertEqual(self.generate_output('  0/50 [>---------------------------]   0%')
                         + self.generate_output('  1/50 [>---------------------------]   2%')
                         + self.generate_output('  2/50 [=>--------------------------]   4%'),
                         output.get_stream().read())

    def get_output_stream(self):
        stream = StringIO.StringIO()

        return StreamOutput(stream)

    def generate_output(self, expected):
        expected_out = expected

        if self.last_messages_length is not None:
            expected_out = '\x20' * self.last_messages_length + '\x0D' + expected

        self.last_messages_length = len(expected)

        return '\x0D' + expected_out
