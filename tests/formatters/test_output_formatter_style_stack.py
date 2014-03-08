# -*- coding: utf-8 -*-

from cleo.formatters import OutputFormatterStyle, OutputFormatterStyleStack

from .. import CleoTestCase


class OutputFormatterStyleStackTest(CleoTestCase):

    def test_push(self):
        stack = OutputFormatterStyleStack()
        s1 = OutputFormatterStyle('white', 'black')
        s2 = OutputFormatterStyle('yellow', 'blue')
        stack.push(s1)
        stack.push(s2)

        self.assertEqual(s2, stack.get_current())

        s3 = OutputFormatterStyle('green', 'red')
        stack.push(s3)

        self.assertEqual(s3, stack.get_current())

    def test_pop(self):
        stack = OutputFormatterStyleStack()
        s1 = OutputFormatterStyle('white', 'black')
        s2 = OutputFormatterStyle('yellow', 'blue')
        stack.push(s1)
        stack.push(s2)

        self.assertEqual(s2, stack.pop())
        self.assertEqual(s1, stack.pop())

    def test_pop_empty(self):
        stack = OutputFormatterStyleStack()

        self.assertTrue(isinstance(stack.pop(), OutputFormatterStyle))

    def test_pop_not_last(self):
        stack = OutputFormatterStyleStack()
        s1 = OutputFormatterStyle('white', 'black')
        s2 = OutputFormatterStyle('yellow', 'blue')
        s3 = OutputFormatterStyle('green', 'red')
        stack.push(s1)
        stack.push(s2)
        stack.push(s3)

        self.assertEqual(s2, stack.pop(s2))
        self.assertEqual(s1, stack.pop())

    def test_invalid_pop(self):
        stack = OutputFormatterStyleStack()
        s1 = OutputFormatterStyle('white', 'black')
        s2 = OutputFormatterStyle('yellow', 'blue')
        stack.push(s1)

        self.assertRaises(
            Exception,
            stack.pop,
            s2
        )


