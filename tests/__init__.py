# -*- coding: utf-8 -*-

import sys
from unittest import TestCase

PY3 = sys.version_info[0] == 3

if PY3:
    import unittest.mock as mock
else:
    import mock


class CleoTestCase(TestCase):

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
