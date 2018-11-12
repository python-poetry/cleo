# -*- coding: utf-8 -*-

import os
from .. import CleoTestCase
from .objects_provider import ObjectsProvider
from cleo.outputs import BufferedOutput
from cleo.commands import BaseCommand


class DescriptorTestCase(CleoTestCase):
    def setUp(self):
        super(DescriptorTestCase, self).setUp()

        self.original = BaseCommand._get_command_full_name
        BaseCommand._get_command_full_name = lambda self: "app/console " + self.name

    def tearDown(self):
        super(DescriptorTestCase, self).tearDown()

        BaseCommand._get_command_full_name = self.original

    def _test_describe_input_arguments(self):
        for argument, expected_description in self.get_input_argument_test_data():
            self.assertDescription(expected_description, argument)

    def _test_describe_input_options(self):
        for option, expected_description in self.get_input_option_test_data():
            self.assertDescription(expected_description, option)

    def _test_describe_input_definitions(self):
        for definition, expected_description in self.get_input_definition_test_data():
            self.assertDescription(expected_description, definition)

    def _test_describe_commands(self):
        for command, expected_description in self.get_command_test_data():
            self.assertDescription(expected_description, command)

    def _test_describe_applications(self):
        for application, expected_description in self.get_application_test_data():
            self.assertDescription(expected_description, application)

    def get_input_argument_test_data(self):
        return self.get_description_test_data(ObjectsProvider.get_input_arguments())

    def get_input_option_test_data(self):
        return self.get_description_test_data(ObjectsProvider.get_input_options())

    def get_input_definition_test_data(self):
        return self.get_description_test_data(ObjectsProvider.get_input_definitions())

    def get_command_test_data(self):
        return self.get_description_test_data(ObjectsProvider.get_commands())

    def get_application_test_data(self):
        return self.get_description_test_data(ObjectsProvider.get_applications())

    def get_description_test_data(self, objects):
        data = []
        for name, obj in objects.items():
            description = self.open_fixture("%s.%s" % (name, self.get_format()))
            data.append((obj, description))

        return data

    def assertDescription(self, expected_description, described_object):
        output = BufferedOutput(BufferedOutput.VERBOSITY_NORMAL, True)
        self.get_descriptor().describe(output, described_object, raw_output=True)
        fetched = output.fetch().replace(os.linesep, "\n").strip()

        self.assertEqual(expected_description.strip(), fetched)
