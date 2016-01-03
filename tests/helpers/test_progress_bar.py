# -*- coding: utf-8 -*-

from io import BytesIO

import os
from unittest import TestCase
from cleo.helpers import ProgressBar
from cleo.outputs.stream_output import StreamOutput
from cleo._compat import decode


class ProgressBarTest(TestCase):

    def test_multiple_start(self):
        output = self.get_output_stream()
        bar = ProgressBar(output)
        bar.start()
        bar.advance()
        bar.start()

        expected = self.generate_output(
            [
                '    0 [>---------------------------]',
                '    1 [->--------------------------]',
                '    0 [>---------------------------]'
            ]
        )

        self.assertEqual(expected, self.get_output_content(output))

    def test_advance(self):
        output = self.get_output_stream()
        bar = ProgressBar(output)
        bar.start()
        bar.advance()

        expected = self.generate_output([
            [
                '    0 [>---------------------------]',
                '    1 [->--------------------------]'
            ]
        ])

        self.assertEqual(expected, self.get_output_content(output))

    def test_advance_with_step(self):
        output = self.get_output_stream()
        bar = ProgressBar(output)
        bar.start()
        bar.advance(5)

        expected = self.generate_output([
            [
                '    0 [>---------------------------]',
                '    5 [----->----------------------]'
            ]
        ])

        self.assertEqual(expected, self.get_output_content(output))

    def test_advance_multiple_times(self):
        output = self.get_output_stream()
        bar = ProgressBar(output)
        bar.start()
        bar.advance(3)
        bar.advance(2)

        expected = self.generate_output([
            [
                '    0 [>---------------------------]',
                '    3 [--->------------------------]',
                '    5 [----->----------------------]'
            ]
        ])

        self.assertEqual(expected, self.get_output_content(output))

    def test_advance_over_max(self):
        output = self.get_output_stream()
        bar = ProgressBar(output, 10)
        bar.set_progress(9)
        bar.advance()
        bar.advance()

        expected = self.generate_output([
            [
                '  9/10 [=========================>--]  90%',
                ' 10/10 [============================] 100%',
                ' 11/11 [============================] 100%'
            ]
        ])

        self.assertEqual(expected, self.get_output_content(output))

    def test_format(self):
        expected = self.generate_output([
            '  0/10 [>---------------------------]   0%',
            ' 10/10 [============================] 100%',
            ' 10/10 [============================] 100%'
        ])

        # max in construct, no format
        output = self.get_output_stream()
        bar = ProgressBar(output, 10)
        bar.start()
        bar.advance(10)
        bar.finish()

        self.assertEqual(expected, self.get_output_content(output))

        # max in start, no format
        output = self.get_output_stream()
        bar = ProgressBar(output)
        bar.start(10)
        bar.advance(10)
        bar.finish()

        self.assertEqual(expected, self.get_output_content(output))

        # max in construct, explicit format before
        output = self.get_output_stream()
        bar = ProgressBar(output, 10)
        bar.set_format('normal')
        bar.start()
        bar.advance(10)
        bar.finish()

        self.assertEqual(expected, self.get_output_content(output))

        # max in start, explicit format before
        output = self.get_output_stream()
        bar = ProgressBar(output)
        bar.set_format('normal')
        bar.start(10)
        bar.advance(10)
        bar.finish()

        self.assertEqual(expected, self.get_output_content(output))

    def test_customizations(self):
        output = self.get_output_stream()
        bar = ProgressBar(output, 10)
        bar.set_bar_width(10)
        bar.set_bar_character('_')
        bar.set_empty_bar_character(' ')
        bar.set_progress_character('/')
        bar.set_format(' %current%/%max% [%bar%] %percent:3s%%')
        bar.start()
        bar.advance()

        expected = self.generate_output([
            '  0/10 [/         ]   0%',
            '  1/10 [_/        ]  10%'
        ])

        self.assertEqual(expected, self.get_output_content(output))

    def test_display_without_start(self):
        output = self.get_output_stream()
        bar = ProgressBar(output, 50)
        bar.display()

        expected = self.generate_output('  0/50 [>---------------------------]   0%')

        self.assertEqual(expected, self.get_output_content(output))

    def test_display_with_quiet_verbosity(self):
        output = self.get_output_stream(verbosity=StreamOutput.VERBOSITY_QUIET)
        bar = ProgressBar(output, 50)
        bar.display()

        self.assertEqual('', self.get_output_content(output))

    def test_finish_without_start(self):
        output = self.get_output_stream()
        bar = ProgressBar(output, 50)
        bar.finish()

        expected = self.generate_output(' 50/50 [============================] 100%')

        self.assertEqual(expected, self.get_output_content(output))

    def test_percent(self):
        output = self.get_output_stream()
        bar = ProgressBar(output, 50)
        bar.start()
        bar.display()
        bar.advance()
        bar.advance()

        expected = self.generate_output([
            '  0/50 [>---------------------------]   0%',
            '  0/50 [>---------------------------]   0%',
            '  1/50 [>---------------------------]   2%',
            '  2/50 [=>--------------------------]   4%',
        ])

        self.assertEqual(expected, self.get_output_content(output))

    def test_overwrite_with_shorter_line(self):
        output = self.get_output_stream()
        bar = ProgressBar(output, 50)
        bar.set_format(' %current%/%max% [%bar%] %percent:3s%%')
        bar.start()
        bar.display()
        bar.advance()

        # Set shorter format
        bar.set_format(' %current%/%max% [%bar%]')
        bar.advance()

        expected = self.generate_output([
            '  0/50 [>---------------------------]   0%',
            '  0/50 [>---------------------------]   0%',
            '  1/50 [>---------------------------]   2%',
            '  2/50 [=>--------------------------]     ',
        ])

        self.assertEqual(expected, self.get_output_content(output))

    def test_set_current_progress(self):
        output = self.get_output_stream()
        bar = ProgressBar(output, 50)
        bar.start()
        bar.display()
        bar.advance()
        bar.set_progress(15)
        bar.set_progress(25)

        expected = self.generate_output([
            '  0/50 [>---------------------------]   0%',
            '  0/50 [>---------------------------]   0%',
            '  1/50 [>---------------------------]   2%',
            ' 15/50 [========>-------------------]  30%',
            ' 25/50 [==============>-------------]  50%',
        ])

        self.assertEqual(expected, self.get_output_content(output))

    def test_multibyte_support(self):
        output = self.get_output_stream()
        bar = ProgressBar(output)
        bar.start()
        bar.set_bar_character('■')
        bar.advance(3)

        expected = self.generate_output([
            '    0 [>---------------------------]',
            '    3 [■■■>------------------------]'
        ])

        self.assertEqual(expected, self.get_output_content(output))

    def test_clear(self):
        output = self.get_output_stream()
        bar = ProgressBar(output, 50)
        bar.start()
        bar.set_progress(25)
        bar.clear()

        expected = self.generate_output([
            '  0/50 [>---------------------------]   0%',
            ' 25/50 [==============>-------------]  50%',
            '                                          '
        ])

        self.assertEqual(expected, self.get_output_content(output))

    def test_percent_not_hundred_before_complete(self):
        output = self.get_output_stream()
        bar = ProgressBar(output, 200)
        bar.start()
        bar.display()
        bar.advance(199)
        bar.advance()

        expected = self.generate_output([
            '   0/200 [>---------------------------]   0%',
            '   0/200 [>---------------------------]   0%',
            ' 199/200 [===========================>]  99%',
            ' 200/200 [============================] 100%',
        ])

        self.assertEqual(expected, self.get_output_content(output))

    def test_non_decorated_output(self):
        output = self.get_output_stream(False)
        bar = ProgressBar(output, 200)
        bar.start()

        for i in range(200):
            bar.advance()

        bar.finish()

        expected = os.linesep.join([
            '   0/200 [>---------------------------]   0%',
            '  20/200 [==>-------------------------]  10%',
            '  40/200 [=====>----------------------]  20%',
            '  60/200 [========>-------------------]  30%',
            '  80/200 [===========>----------------]  40%',
            ' 100/200 [==============>-------------]  50%',
            ' 120/200 [================>-----------]  60%',
            ' 140/200 [===================>--------]  70%',
            ' 160/200 [======================>-----]  80%',
            ' 180/200 [=========================>--]  90%',
            ' 200/200 [============================] 100%',
        ])

        self.assertEqual(expected, self.get_output_content(output))

    def get_output_stream(self, decorated=True, verbosity=StreamOutput.VERBOSITY_NORMAL):
        stream = BytesIO()

        return StreamOutput(stream, decorated=decorated, verbosity=verbosity)

    def generate_output(self, expected):
        if isinstance(expected, list):
            expected_out = ''

            for exp in expected:
                expected_out += self.generate_output(exp)
        else:
            count = expected.count('\n')

            expected_out = '\x0D'
            if count:
                expected_out += '\033[%dA' % count

            expected_out += expected

        return decode(expected_out)

    def get_output_content(self, output):
        output.get_stream().seek(0)

        value = output.get_stream().getvalue()

        return decode(value)
