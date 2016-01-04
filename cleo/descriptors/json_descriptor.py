# -*- coding: utf-8 -*-

import re

try:
    import simplejson as json
except ImportError:
    import json

from collections import OrderedDict

from .descriptor import Descriptor
from .application_description import ApplicationDescription


class JsonDescriptor(Descriptor):

    def _describe_input_argument(self, argument, **options):
        """
        Describes an InputArgument instance.

        :type argument: InputArgument
        :type options: dict
        """
        self._write_data(self._get_input_argument_data(argument), **options)

    def _describe_input_option(self, option, **options):
        """
        Describes an InputOption instance.

        :type argument: InputOption
        :type options: dict
        """
        self._write_data(self._get_input_option_data(option), **options)

    def _describe_input_definition(self, definition, **options):
        """
        Describes an InputDefinition instance.

        :type argument: InputDefinition
        :type options: dict
        """
        self._write_data(self._get_input_definition_data(definition), **options)

    def _describe_command(self, command, **options):
        """
        Describes a Command instance.

        :type argument: BaseCommand
        :type options: dict
        """
        self._write_data(self._get_command_data(command), **options)

    def _describe_application(self, application, **options):
        """
        Describes an Application instance.

        :type argument: Application
        :type options: dict
        """
        described_namespace = options.get('namespace')
        description = ApplicationDescription(application, described_namespace)
        commands = []

        for command in description.get_commands().values():
            commands.append(self._get_command_data(command))

        if described_namespace:
            data = {
                'commands': commands,
                'namespace': described_namespace
            }
        else:
            data = {
                'commands': commands,
                'namespaces': list(description.get_namespaces().values())
            }

        self._write_data(data, **options)

    def _write_data(self, data, **options):
        actual_options = {
            'separators': (',', ':')
        }

        actual_options.update(options.get('json_encoding', {}))

        self._write(json.dumps(data, **actual_options))

    def _get_input_argument_data(self, argument):
        return OrderedDict([
            ('name', argument.get_name()),
            ('is_required', argument.is_required()),
            ('is_list', argument.is_list()),
            ('description', re.sub('\s*[\r\n]\s*', ' ', argument.get_description())),
            ('default', argument.get_default())
        ])

    def _get_input_option_data(self, option):
        shortcut = ''
        if option.get_shortcut():
            shortcut = '-' + '|-'.join(option.get_shortcut().split('|'))

        return OrderedDict([
            ('name', '--' + option.get_name()),
            ('shortcut', shortcut),
            ('accept_value', option.accept_value()),
            ('is_value_required', option.is_value_required()),
            ('is_multiple', option.is_list()),
            ('description', re.sub('\s*[\r\n]\s*', ' ', option.get_description())),
            ('default', option.get_default())
        ])

    def _get_input_definition_data(self, definition):
        arguments = OrderedDict()
        for argument in definition.get_arguments():
            arguments[argument.get_name()] = self._get_input_argument_data(argument)

        options = OrderedDict()
        for option in definition.get_options():
            options[option.get_name()] = self._get_input_option_data(option)

        return OrderedDict([
            ('arguments', arguments),
            ('options', options)
        ])

    def _get_command_data(self, command):
        command.get_synopsis()
        command.merge_application_definition(False)

        return OrderedDict([
            ('name', command.get_name()),
            ('usage', [command.get_synopsis()] + command.get_aliases() + command.get_usages()),
            ('description', command.get_description()),
            ('help', command.get_processed_help()),
            ('definition', self._get_input_definition_data(command.get_native_definition()))
        ])

