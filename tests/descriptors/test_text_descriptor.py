# -*- coding: utf-8 -*-

from . import DescriptorTestCase
from cleo.descriptors import TextDescriptor


class TextDescriptorTestCase(DescriptorTestCase):
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
        return TextDescriptor()

    def get_format(self):
        return "txt"
