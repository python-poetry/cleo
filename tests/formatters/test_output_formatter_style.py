# -*- coding: utf-8 -*-

from cleo.formatters import OutputFormatterStyle

from .. import CleoTestCase


class OutputFormatterStyleTest(CleoTestCase):

    def test_init(self):
        style = OutputFormatterStyle('green', 'black', ['bold', 'underscore'])
        self.assertEqual('\033[32;40;1;4mfoo\033[0m', style.apply('foo'))

        style = OutputFormatterStyle('red', None, ['blink'])
        self.assertEqual('\033[31;5mfoo\033[0m', style.apply('foo'))

        style = OutputFormatterStyle(None, 'white')
        self.assertEqual('\033[47mfoo\033[0m', style.apply('foo'))

    def test_foreground(self):
        style = OutputFormatterStyle()

        style.set_foreground('black')
        self.assertEqual('\033[30mfoo\033[0m', style.apply('foo'))

        style.set_foreground('blue')
        self.assertEqual('\033[34mfoo\033[0m', style.apply('foo'))

        self.assertRaises(
            Exception,
            style.set_foreground,
            'undefined-color'
        )

    def test_background(self):
        style = OutputFormatterStyle()

        style.set_background('black')
        self.assertEqual('\033[40mfoo\033[0m', style.apply('foo'))

        style.set_background('yellow')
        self.assertEqual('\033[43mfoo\033[0m', style.apply('foo'))

        self.assertRaises(
            Exception,
            style.set_background,
            'undefined-color'
        )

    def test_options(self):
        style = OutputFormatterStyle()

        style.set_options(['reverse', 'conceal'])
        self.assertEqual('\033[7;8mfoo\033[0m', style.apply('foo'))

        style.set_option('bold')
        self.assertEqual('\033[7;8;1mfoo\033[0m', style.apply('foo'))

        style.unset_option('reverse')
        self.assertEqual('\033[8;1mfoo\033[0m', style.apply('foo'))

        style.set_option('bold')
        self.assertEqual('\033[8;1mfoo\033[0m', style.apply('foo'))

        style.set_options(['bold'])
        self.assertEqual('\033[1mfoo\033[0m', style.apply('foo'))

        self.assertRaisesRegexp(
            Exception,
            'Invalid option specified: "foo"',
            style.set_option,
            'foo'
        )

        self.assertRaisesRegexp(
            Exception,
            'Invalid option specified: "foo"',
            style.unset_option,
            'foo'
        )
