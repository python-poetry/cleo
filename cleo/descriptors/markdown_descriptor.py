# -*- coding: utf-8 -*-

import re
from .descriptor import Descriptor
from .application_description import ApplicationDescription


class MarkdownDescriptor(Descriptor):

    def _describe_input_argument(self, argument, **options):
        """
        Describes an InputArgument instance.

        :type argument: InputArgument
        :type options: dict
        """
        name = argument.get_name() or '<none>'
        required = 'yes' if argument.is_required() else 'no'
        is_list = 'yes' if argument.is_list() else 'no'
        description = re.sub('\s*[\r\n]\s*', '\n  ', argument.get_description() or '<none>')
        default = argument.get_default()

        lines = [
            '**%s:**\n\n' % name,
            '* Name: %s\n' % name,
            '* Is required: %s\n' % required,
            '* Is list: %s\n' % is_list,
            '* Description: %s\n' % description,
            '* Default: `%s`' % default
        ]

        self._write_lines(lines)

    def _describe_input_option(self, option, **options):
        """
        Describes an InputOption instance.

        :type argument: InputOption
        :type options: dict
        """
        name = option.get_name() or '<none>'
        shortcut = '<none>'
        if option.get_shortcut():
            shortcut = '`-' + '|-'.join(option.get_shortcut().split('|')) + '`'

        value_required = 'yes' if option.is_value_required() else 'no'
        accept_value = 'yes' if option.accept_value() else 'no'
        is_multiple = 'yes' if option.is_list() else 'no'
        description = re.sub('\s*[\r\n]\s*', '\n  ', option.get_description() or '<none>')
        default = option.get_default()

        lines = [
            '**%s:**\n\n' % name,
            '* Name: `--%s`\n' % name,
            '* Shortcut: %s\n' % shortcut,
            '* Accept value: %s\n' % accept_value,
            '* Is value required: %s\n' % value_required,
            '* Is multiple: %s\n' % is_multiple,
            '* Description: %s\n' % description,
            '* Default: `%s`' % default
        ]

        self._write_lines(lines)

    def _describe_input_definition(self, definition, **options):
        """
        Describes an InputDefinition instance.

        :type argument: InputDefinition
        :type options: dict
        """
        if definition.get_arguments():
            self._write('### Arguments:')
            for argument in definition.get_arguments():
                self._write('\n\n')
                self._describe_input_argument(argument)

        if definition.get_options():
            if definition.get_arguments():
                self._write('\n\n')

            self._write('### Options:')
            for option in definition.get_options():
                self._write('\n\n')
                self._describe_input_option(option)

    def _describe_command(self, command, **options):
        """
        Describes a Command instance.

        :type argument: BaseCommand
        :type options: dict
        """
        command.get_synopsis()
        command.merge_application_definition(False)

        usages = [command.get_synopsis()] + command.get_aliases() + command.get_usages()

        lines = [
            '%s\n' % command.get_name(),
            '%s\n\n' % ('-' * len(command.get_name())),
            '* Description: %s\n' % (command.get_description() or '<none>'),
            '* Usage:\n\n%s' % (''.join(list(map(lambda x: '  * `%s`\n' % x, usages))))
        ]

        self._write_lines(lines)

        help = command.get_processed_help()
        if help:
            self._write('\n')
            self._write(help)

        if command.get_native_definition():
            self._write('\n\n')
            self._describe_input_definition(command.get_native_definition())

    def _describe_application(self, application, **options):
        """
        Describes an Application instance.

        :type argument: Application
        :type options: dict
        """
        described_namespace = options.get('namespace')
        description = ApplicationDescription(application, described_namespace)

        self._write('%s\n%s' % (application.get_name(), '=' * len(application.get_name())))

        for namespace in description.get_namespaces().values():
            if namespace['id'] != ApplicationDescription.GLOBAL_NAMESPACE:
                self._write('\n\n')
                self._write('**%s:**' % namespace['id'])

            self._write('\n\n')
            self._write('\n'.join(list(map(lambda x: '* %s' % x, namespace['commands']))))

        for command in description.get_commands().values():
            self._write('\n\n')
            self._describe_command(command)

    def _write_lines(self, lines, **options):
        for line in lines:
            self._write(line, **options)
