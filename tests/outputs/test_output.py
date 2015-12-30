# -*- coding: utf-8 -*-


from cleo.outputs import Output
from cleo.formatters import OutputFormatterStyle

from .. import CleoTestCase


class OutputTest(CleoTestCase):

    def test_init(self):
        output = MyOutput(Output.VERBOSITY_QUIET, True)
        self.assertEqual(Output.VERBOSITY_QUIET, output.get_verbosity())
        self.assertTrue(output.is_decorated())

    def test_set_is_decorated(self):
        output = MyOutput()
        output.set_decorated(True)
        self.assertTrue(output.is_decorated())

    def test_set_get_verbosity(self):
        output = MyOutput()
        output.set_verbosity(Output.VERBOSITY_QUIET)
        self.assertEqual(Output.VERBOSITY_QUIET, output.get_verbosity())

        self.assertTrue(output.is_quiet())
        self.assertFalse(output.is_verbose())

        output.set_verbosity(Output.VERBOSITY_NORMAL)
        self.assertFalse(output.is_quiet())
        self.assertFalse(output.is_verbose())

        output.set_verbosity(Output.VERBOSITY_VERBOSE)
        self.assertFalse(output.is_quiet())
        self.assertTrue(output.is_verbose())

    def test_write_with_verbosity_quiet(self):
        output = MyOutput(Output.VERBOSITY_QUIET)
        output.writeln('foo')
        self.assertEqual('', output.output)

    def test_write_a_list_of_messages(self):
        output = MyOutput()
        output.writeln(['foo', 'bar'])
        self.assertEqual('foo\nbar\n', output.output)

    def test_write_raw_message(self):
        for message, type_, expected_output in self.provide_write_arguments():
            output = MyOutput()
            output.writeln(message, type_)
            self.assertEqual(expected_output, output.output)

    def provide_write_arguments(self):
        return [
            (
                '<info>foo</info>',
                Output.OUTPUT_RAW,
                '<info>foo</info>\n'
            ),
            (
                '<info>foo</info>',
                Output.OUTPUT_PLAIN,
                'foo\n'
            )
        ]

    def test_write_with_decoration_turned_off(self):
        output = MyOutput()
        output.set_decorated(False)
        output.writeln('<info>foo</info>')
        self.assertEqual('foo\n', output.output)

    def test_write_decorated_message(self):
        foo_style = OutputFormatterStyle('yellow', 'red', ['blink'])
        output = MyOutput()
        output.get_formatter().set_style('foo', foo_style)
        output.set_decorated(True)
        output.writeln('<foo>foo</foo>')
        self.assertEqual('\033[33;41;5mfoo\033[0m\n', output.output)

    def test_write_with_invalid_output_type(self):
        output = MyOutput()
        self.assertRaisesRegexp(
            Exception,
            'Unknown output type given \(24\)',
            output.writeln,
            '<foo>foo</foo>',
            24
        )

    def test_write_with_invalid_style(self):
        output = MyOutput()

        output.clear()
        output.write('<bar>foo</bar>')
        self.assertEqual('<bar>foo</bar>', output.output)

        output.clear()
        output.writeln('<bar>foo</bar>')
        self.assertEqual('<bar>foo</bar>\n', output.output)


class MyOutput(Output):

    def __init__(self, verbosity=Output.VERBOSITY_NORMAL, decorated=None, formatter=None):
        super(MyOutput, self).__init__(verbosity, decorated, formatter)

        self.output = ''

    def clear(self):
        self.output = ''

    def do_write(self, message, newline):
        self.output += '%s%s' % (message, "\n" if newline else '')
