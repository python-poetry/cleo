# -*- coding: utf-8 -*-

from io import BytesIO

from unittest import TestCase
from cleo.helpers.progress_helper import ProgressHelper
from cleo.outputs.stream_output import StreamOutput


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
                         output.get_stream().read().decode())

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
                         output.get_stream().read().decode())

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
                         output.get_stream().read().decode())

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
                         output.get_stream().read().decode())

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
                         output.get_stream().read().decode())

    def test_colored_bar(self):
        """
        Colored progressbar
        """
        progress = ProgressHelper()
        output = self.get_output_stream(decorated=True)
        progress.set_bar_character('<comment>=</comment>')
        progress.start(output, 50)
        progress.display()
        progress.advance()
        progress.advance()
        progress.advance()
        progress.advance()
        progress.advance()

        output.get_stream().seek(0)
        self.assertEqual(self.generate_output('  0/50 [>---------------------------]   0%')
                         + self.generate_output('  1/50 [>---------------------------]   2%')
                         + self.generate_output('  2/50 [\x1b[33m=\x1b[0m>--------------------------]   4%')
                         + self.generate_output('  3/50 [\x1b[33m=\x1b[0m>--------------------------]   6%')
                         + self.generate_output('  4/50 [\x1b[33m=\x1b[0m\x1b[33m=\x1b[0m>-------------------------]   8%')
                         + self.generate_output('  5/50 [\x1b[33m=\x1b[0m\x1b[33m=\x1b[0m>-------------------------]  10%'),
                         output.get_stream().read().decode())

    def get_output_stream(self, decorated=None):
        stream = BytesIO()

        return StreamOutput(stream, decorated=decorated)

    def generate_output(self, expected):
        expected_out = expected

        if self.last_messages_length is not None:
            expected_out = expected.ljust(self.last_messages_length, '\x20')

        self.last_messages_length = len(expected)

        return '\x0D' + expected_out
