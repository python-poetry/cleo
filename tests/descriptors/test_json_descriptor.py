# -*- coding: utf-8 -*-

import os

try:
    import simplejson as json
except ImportError:
    import json

from . import DescriptorTestCase
from cleo.descriptors import JsonDescriptor
from cleo.outputs import BufferedOutput


class JsonDescriptorTestCase(DescriptorTestCase):

    def test_describe_input_arguments(self):
        return self._test_describe_input_arguments()

    def test_describe_input_options(self):
        return self._test_describe_input_options()

    def test_describe_input_definitions(self):
        return self._test_describe_input_definitions()

    def test_describe_commands(self):
        return self._test_describe_commands()

    def test_describe_applications(self):
        return self._test_describe_applications()

    def get_descriptor(self):
        return JsonDescriptor()

    def get_format(self):
        return 'json'

    def assertDescription(self, expected_description, described_object):
        output = BufferedOutput(BufferedOutput.VERBOSITY_NORMAL, True)
        self.get_descriptor().describe(output, described_object, raw_output=True)
        fetched = output.fetch().replace(os.linesep, '\n').strip()

        self.assertEqual(json.loads(expected_description), json.loads(fetched))
