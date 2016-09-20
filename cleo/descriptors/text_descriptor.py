# -*- coding: utf-8 -*-

import re

try:
    import simplejson as json
except ImportError:
    import json

from .descriptor import Descriptor
from .application_description import ApplicationDescription
from ..inputs import InputDefinition


class TextDescriptor(Descriptor):
    """
    Text Descriptor
    """
    def _describe_input_argument(self, argument, **options):
        """
        Describes an InputArgument instance.

        :type argument: InputArgument
        :type options: dict
        """
        default = argument.get_default()
        if default is not None and (not isinstance(default, list) or len(default)):
            default = '<comment> [default: %s]</comment>' % self._format_default_value(default)
        else:
            default = ''

        total_width = options.get('total_width', len(argument.get_name()))
        spacing_width = total_width - len(argument.get_name()) + 2

        self._write_text(
            '  <info>%s</info>%s%s%s'
            % (
                argument.get_name(),
                ' ' * spacing_width,
                re.sub('\s*[\r\n]\s*', '\n' + (' ' * (total_width + 17)), argument.get_description() or ''),
                default
            ),
            **options
        )

    def _describe_input_option(self, option, **options):
        """
        Describes an InputOption instance.

        :type argument: InputOption
        :type options: dict
        """
        accept_value = option.accept_value()
        default = option.get_default()
        if accept_value and default is not None and (not isinstance(default, list) or len(default)):
            default = '<comment> [default: %s]</comment>' % self._format_default_value(default)
        else:
            default = ''

        value = ''
        if accept_value:
            value = '=%s' % option.get_name().upper()

            if option.is_value_optional():
                value = '[%s]' % value

        total_width = options.get('total_width', self._calculate_total_width_for_options([option]))
        shortcut = option.get_shortcut()
        synopsis = '%s%s'\
                   % ('-%s, ' % shortcut if shortcut else '    ',
                      '--%s%s' % (option.get_name(), value))

        spacing_width = total_width - len(synopsis) + 2

        self._write_text(
            '  <info>%s</info>%s%s%s%s'
            % (
                synopsis,
                ' ' * spacing_width,
                re.sub('\s*[\r\n]\s*', '\n' + (' ' * (total_width + 17)), option.get_description() or ''),
                default,
                '<comment> (multiple values allowed)</comment>' if option.is_list() else ''
            ),
            **options
        )

    def _describe_input_definition(self, definition, **options):
        """
        Describes an InputDefinition instance.

        :type argument: InputDefinition
        :type options: dict
        """
        definition_options = definition.get_options()
        definition_arguments = definition.get_arguments()
        total_width = self._calculate_total_width_for_options(definition_options)

        for argument in definition_arguments:
            total_width = max(total_width, len(argument.get_name()))

        if definition_arguments:
            self._write_text('<comment>Arguments:</comment>', **options)
            self._write_text('\n')

            for argument in definition_arguments:
                self._describe_input_argument(argument, total_width=total_width, **options)
                self._write_text('\n')

        if definition_arguments and definition_options:
            self._write_text('\n')

        if definition_options:
            later_options = []

            self._write_text('<comment>Options:</comment>', **options)

            for option in definition_options:
                if option.get_shortcut() and len(option.get_shortcut()) > 1:
                    later_options.append(option)
                    continue

                self._write_text('\n')
                self._describe_input_option(option, total_width=total_width, **options)

            for option in later_options:
                self._write_text('\n')
                self._describe_input_option(option, total_width=total_width, **options)

    def _describe_command(self, command, **options):
        """
        Describes a Command instance.

        :type argument: BaseCommand
        :type options: dict
        """
        command.get_synopsis(True)
        command.get_synopsis(False)
        command.merge_application_definition(False)

        self._write_text('<comment>Usage:</comment>', **options)
        for usage in [command.get_synopsis(True)] + command.get_aliases() + command.get_usages():
            self._write_text('\n')
            self._write_text('  %s' % usage, **options)

        self._write_text('\n')

        definition = command.get_native_definition()
        if definition.get_options() or definition.get_arguments():
            self._write_text('\n')
            self._describe_input_definition(definition, **options)
            self._write_text('\n')

        help = command.get_processed_help()
        if help:
            self._write_text('\n')
            self._write_text('<comment>Help:</comment>', **options)
            self._write_text('\n')
            self._write_text(' %s' % help.replace('\n', '\n '), **options)
            self._write_text('\n')

    def _describe_application(self, application, **options):
        """
        Describes an Application instance.

        :type argument: Application
        :type options: dict
        """
        described_namespace = options.get('namespace')
        description = ApplicationDescription(application, described_namespace)

        raw_text = options.get('raw_text')
        if raw_text:
            width = self._get_column_width(description.get_commands().values())

            for command in description.get_commands().values():
                self._write_text('%-*s %s' % (width, command.get_name(), command.get_description()), **options)
                self._write_text('\n')
        else:
            help = application.get_help()
            if help:
                self._write_text('%s\n\n' % help, **options)

            self._write_text('<comment>Usage:</comment>\n', **options)
            self._write_text('  command [options] [arguments]\n\n', **options)

            self._describe_input_definition(
                InputDefinition(
                    application.get_definition().get_options()
                ),
                **options
            )

            self._write_text('\n')
            self._write_text('\n')

            width = self._get_column_width(description.get_commands().values())

            if described_namespace:
                self._write_text(
                    '<comment>Available commands for the "%s" namespace:</comment>'
                    % described_namespace,
                    **options
                )
            else:
                self._write_text('<comment>Available commands:</comment>', **options)

            # add commands by namespace
            commands = description.get_commands()

            for namespace in description.get_namespaces().values():
                if not described_namespace and namespace['id'] != ApplicationDescription.GLOBAL_NAMESPACE:
                    self._write_text('\n')
                    self._write_text(' <comment>%s</comment>' % namespace['id'], **options)

                for name in namespace['commands']:
                    if name in commands:
                        self._write_text('\n')
                        spacing_width = width - len(name)
                        command = commands[name]
                        command_aliases = self._get_command_aliases_text(command)
                        desc = description.get_command(name).get_description()

                        self._write_text(
                            '  <info>%s</info>%s%s'
                            % (name, ' ' * spacing_width, command_aliases + desc),
                            **options
                        )

        self._write_text('\n')

    def _get_command_aliases_text(self, command):
        """
        Formats command aliases to show them in the command description.

        :param command: The command
        :type command: Command

        :rtype: str
        """
        text = ''
        aliases = command.get_aliases()

        if aliases:
            text = '[{}] '.format('|'.join(aliases))

        return text

    def _write_text(self, content, **options):
        raw = options.get('raw_text')
        if raw:
            content = re.sub(r'<[^>]*?>', '', content)

        self._write(content, not options.get('raw_output', False))

    def _format_default_value(self, default):
        """
        Formats input option/argument default value.

        :type default: mixed

        :rtype: str
        """
        return json.dumps(default)

    def _get_column_width(self, commands):
        widths = []

        for command in commands:
            widths.append(len(command.get_name()))
            for alias in command.get_aliases():
                widths.append(len(alias))

        return max(widths) + 2

    def _calculate_total_width_for_options(self, options):
        total_width = 0

        for option in options:
            # "-" + shortcut + ", --" + name
            shortcut = option.get_shortcut() or ''
            name_length = 1 + max(len(shortcut), 1) + 4 + len(option.get_name())

            if option.accept_value():
                value_length = 1 + len(option.get_name())
                if option.is_value_optional():
                    value_length += 2

                name_length += value_length

            total_width = max(total_width, name_length)

        return total_width

