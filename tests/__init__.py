# -*- coding: utf-8 -*-

import sys
import os
from unittest import TestCase

PY3 = sys.version_info[0] == 3

if PY3:
    import unittest.mock as mock
else:
    import mock


class CleoTestCase(TestCase):
    def setUp(self):
        self.fixtures_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "fixtures"
        )
        os.environ["COLUMNS"] = "80"
        os.environ["LINES"] = "24"

    def assertRegex(self, *args, **kwargs):
        if PY3:
            return super(CleoTestCase, self).assertRegex(*args, **kwargs)
        else:
            return self.assertRegexpMatches(*args, **kwargs)

    def assertNotRegex(self, *args, **kwargs):
        if PY3:
            return super(CleoTestCase, self).assertNotRegex(*args, **kwargs)
        else:
            return self.assertNotRegexpMatches(*args, **kwargs)

    def mock(self):
        return mock

    def open_fixture(self, fixture):
        with open(os.path.join(self.fixtures_path, fixture)) as fh:
            return fh.read()
