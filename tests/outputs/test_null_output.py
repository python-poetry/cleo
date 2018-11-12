# -*- coding: utf-8 -*-

from cleo.outputs import Output, NullOutput

from .. import CleoTestCase


class NullOutputTest(CleoTestCase):
    def test_init(self):
        output = NullOutput()

        self.assertFalse(output.is_decorated())

    def test_verbosity(self):
        output = NullOutput()
        self.assertEqual(Output.VERBOSITY_QUIET, output.get_verbosity())

        output.set_verbosity(Output.VERBOSITY_VERBOSE)
        self.assertEqual(Output.VERBOSITY_QUIET, output.get_verbosity())
