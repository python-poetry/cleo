# -*- coding: utf-8 -*-

from io import BytesIO

from cleo.output import Output, StreamOutput

from .. import CleoTestCase


class StreamOutputTest(CleoTestCase):

    def setUp(self):
        self.stream = BytesIO()

    def tearDown(self):
        self.stream = None

    def test_init(self):
        output = StreamOutput(self.stream, Output.VERBOSITY_QUIET, True)
        self.assertEqual(Output.VERBOSITY_QUIET, output.get_verbosity())
        self.assertTrue(output.is_decorated())

    def test_stream_is_required(self):
        self.assertRaisesRegexp(
            Exception,
            'The StreamOutput class needs a stream as its first argument.',
            StreamOutput,
            'foo'
        )

    def test_get_stream(self):
        output = StreamOutput(self.stream)
        self.assertEqual(self.stream, output.get_stream())

    def test_do_write(self):
        output = StreamOutput(self.stream)
        output.writeln('foo')
        output.get_stream().seek(0)
        self.assertEqual('foo\n', output.get_stream().read().decode('utf-8'))
