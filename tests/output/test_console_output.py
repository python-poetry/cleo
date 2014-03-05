# -*- coding: utf-8 -*-

from cleo.output import Output, ConsoleOutput

from .. import CleoTestCase


class ConsoleOutputTest(CleoTestCase):

    def test_init(self):
        output = ConsoleOutput(Output.VERBOSITY_QUIET, True)

        self.assertEqual(Output.VERBOSITY_QUIET, output.get_verbosity())
