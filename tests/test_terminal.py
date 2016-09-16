# -*- coding: utf-8 -*-

import os
from . import CleoTestCase
from cleo.terminal import Terminal


class TerminalTest(CleoTestCase):

    def test_dimensions(self):
        os.environ['COLUMNS'] = '100'
        os.environ['LINES'] = '50'

        terminal = Terminal()
        self.assertEqual(100, terminal.width)
        self.assertEqual(50, terminal.height)
