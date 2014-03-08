# -*- coding: utf-8 -*-

from unittest import TestCase
from cleo.testers.application_tester import ApplicationTester
from cleo.application import Application
from cleo.outputs.output import Output


class TestApplicationTester(TestCase):

    def setUp(self):
        self.application = Application()
        self.application.set_auto_exit(False)
        self.application.register('foo')\
            .add_argument('foo')\
            .set_code(lambda input_, output_: output_.writeln('foo'))

        self.tester = ApplicationTester(self.application)
        self.tester.run(
            [
                ('command', 'foo'),
                ('foo', 'bar')
            ],
            {
                'interactive': False,
                'decorated': False,
                'verbosity': Output.VERBOSITY_VERBOSE
            }
        )

    def tearDown(self):
        self.application = None
        self.tester = None

    def test_run(self):
        """
        ApplicationTester.run() behaves properly
        """
        self.assertFalse(self.tester.get_input().is_interactive(),
                         msg='.run() takes an interactive option.')
        self.assertFalse(self.tester.get_output().is_decorated(),
                         msg='.run() takes a decorated option.')
        self.assertEqual(Output.VERBOSITY_VERBOSE, self.tester.get_output().get_verbosity(),
                         msg='.run() takes an interactive option.')

    def test_get_input(self):
        """
        ApplicationTester.get_input() behaves properly
        """
        self.assertEqual('bar', self.tester.get_input().get_argument('foo'),
                         msg='.get_input() returns the current input instance.')

    def test_get_output(self):
        """
        ApplicationTester.get_output() behaves properly
        """
        self.tester.get_output().get_stream().seek(0)
        self.assertEqual('foo\n', self.tester.get_output().get_stream().read().decode('utf-8'),
                         msg='.get_output() returns the current output instance.')

    def test_get_display(self):
        """
        ApplicationTester.get_display() behaves properly
        """
        self.assertEqual('foo\n', self.tester.get_display(),
                         msg='.get_display() returns the display of the last execution.')
