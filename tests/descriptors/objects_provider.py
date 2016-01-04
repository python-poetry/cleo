# -*- coding: utf-8 -*-

from cleo.inputs import InputArgument, InputOption, InputDefinition
from cleo.commands import Command
from cleo.application import Application
from ..fixtures.descriptor_command_1 import DescriptorCommand1
from ..fixtures.descriptor_command_2 import DescriptorCommand2
from ..fixtures.descriptor_application_1 import DescriptorApplication1
from ..fixtures.descriptor_application_2 import DescriptorApplication2


class ObjectsProvider(object):

    @classmethod
    def get_input_arguments(cls):
        return {
            'input_argument_1': InputArgument('argument_name', InputArgument.REQUIRED),
            'input_argument_2': InputArgument('argument_name', InputArgument.IS_LIST, 'argument description'),
            'input_argument_3': InputArgument('argument_name', InputArgument.OPTIONAL, 'argument description', 'default_value'),
            'input_argument_4': InputArgument('argument_name', InputArgument.REQUIRED, 'multiline\nargument description'),
        }

    @classmethod
    def get_input_options(cls):
        return {
            'input_option_1': InputOption('option_name', 'o', InputOption.VALUE_NONE),
            'input_option_2': InputOption('option_name', 'o', InputOption.VALUE_OPTIONAL, 'option description', 'default_value'),
            'input_option_3': InputOption('option_name', 'o', InputOption.VALUE_REQUIRED, 'option description'),
            'input_option_4': InputOption('option_name', 'o', InputOption.VALUE_IS_LIST | InputOption.VALUE_OPTIONAL, 'option description'),
            'input_option_5': InputOption('option_name', 'o', InputOption.VALUE_REQUIRED, 'multiline\noption description'),
            'input_option_6': InputOption('option_name', ['o', 'O'], InputOption.VALUE_REQUIRED, 'option with multiple shortcuts'),
        }

    @classmethod
    def get_input_definitions(cls):
        return {
            'input_definition_1': InputDefinition(),
            'input_definition_2': InputDefinition([InputArgument('argument_name', InputArgument.REQUIRED)]),
            'input_definition_3': InputDefinition([InputOption('option_name', 'o', InputOption.VALUE_NONE)]),
            'input_definition_4': InputDefinition([
                InputArgument('argument_name', InputArgument.REQUIRED),
                InputOption('option_name', 'o', InputOption.VALUE_NONE)
            ])
        }

    @classmethod
    def get_commands(cls):
        return {
            'command_1': DescriptorCommand1(),
            'command_2': DescriptorCommand2()
        }

    @classmethod
    def get_applications(cls):
        return {
            'application_1': DescriptorApplication1(),
            'application_2': DescriptorApplication2()
        }
