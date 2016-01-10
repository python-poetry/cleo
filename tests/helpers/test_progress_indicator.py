# -*- coding: utf-8 -*-

import time
import os
from io import BytesIO
from cleo.outputs.stream_output import StreamOutput
from cleo._compat import decode
from cleo.helpers.progress_indicator import ProgressIndicator
from .. import CleoTestCase


class ProgressIndicatorTestCase(CleoTestCase):

    def test_default_indicator(self):
        output = self.get_output_stream()
        bar = ProgressIndicator(output)
        bar.start('Starting...')
        time.sleep(0.101)
        bar.advance()
        time.sleep(0.101)
        bar.advance()
        time.sleep(0.101)
        bar.advance()
        time.sleep(0.101)
        bar.advance()
        time.sleep(0.101)
        bar.advance()
        time.sleep(0.101)
        bar.set_message('Advancing...')
        bar.advance()
        bar.finish('Done...')
        bar.start('Starting Again...')
        time.sleep(0.101)
        bar.advance()
        bar.finish('Done Again...')

        expected = self.generate_output([
            ' - Starting...',
            ' \\ Starting...',
            ' | Starting...',
            ' / Starting...',
            ' - Starting...',
            ' \\ Starting...',
            ' \\ Advancing...',
            ' | Advancing...',
            ' | Done...     '
        ])

        expected += os.linesep

        expected += self.generate_output([
            ' - Starting Again...',
            ' \\ Starting Again...',
            ' \\ Done Again...    '
        ])

        expected += os.linesep

        self.assertEqual(
            expected,
            self.get_output_content(output)
        )

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
