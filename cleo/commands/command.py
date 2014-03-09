# -*- coding: utf-8 -*-

import re
import sys

from ..inputs.input import Input
from ..inputs.input_definition import InputDefinition
from ..inputs.input_argument import InputArgument
from ..inputs.input_option import InputOption
from ..outputs.output import Output


class CommandError(Exception):
    pass


class Command(object):

    def __init__(self, name=None):
        self._definition = InputDefinition()
        self._ignore_validation_errors = False
        self._application_definition_merged = False
        self._application_definition_merged_with_args = False
        self._aliases = []
        self._synopsis = None
        self._code = None
        self._help = ''
        self._name = None
        self._application = None
        self._helper_set = None
        self._description = None

        if name is not None:
            self.set_name(name)

        self.configure()

        if not self._name:
            raise Exception('The command name cannot be empty.')

    def ignore_validation_errors(self):
        self._ignore_validation_errors = True

    def set_application(self, application=None):
        self._application = application
        if application:
            self.set_helper_set(application.get_helper_set())
        else:
            self._helper_set = None

    def set_helper_set(self, helper_set):
        self._helper_set = helper_set

    def get_helper_set(self):
        return self._helper_set

    def get_application(self):
        return self._application

    def is_enabled(self):
        return True

    def configure(self):
        pass

    def execute(self, input_, output_):
        raise NotImplementedError()

    def interact(self, input_, output_):
        pass

    def initialize(self, input_, output_):
        pass

    def run(self, input_, output_):
        """
        Runs the command.

        The code to execute is either defined directly with the
        setCode() method or by overriding the execute() method
        in a sub-class.

        @param input_: an Input instance
        @type input_: Input
        @param output_: an Output instance
        @type output_: Output

        @return: The command exit code
        @rtype: int
        """
        # force the creation of the synopsis before the merge with the app definition
        self.get_synopsis()

        # add the application arguments and options
        self.merge_application_definition()

        # bind the input against the command specific arguments/options
        try:
            input_.bind(self._definition)
        except Exception as e:
            if not self._ignore_validation_errors:
                raise

        self.initialize(input_, output_)

        if input_.is_interactive():
            self.interact(input_, output_)

        input_.validate()

        if self._code:
            status_code = self._code(input_, output_)
        else:
            status_code = self.execute(input_, output_)

        try:
            return int(float(status_code))
        except (TypeError, ValueError):
            return 0

    def set_code(self, code):
        if not callable(code):
            raise Exception('Invalid callable provided to Command.setCode().')

        self._code = code

        return self

    def merge_application_definition(self, merge_args=True):
        """
        Merges the application definition with the command definition.

        This method should not be used directly.

        @param merge_args: Whether to merge or not the Application definition arguments to Command definition arguments
        @type merge_args: bool
        """
        if self._application is None \
                or (self._application_definition_merged
                    and (self._application_definition_merged_with_args or not merge_args)):
            return

        if merge_args:
            current_arguments = self._definition.get_arguments()
            self._definition.set_arguments(self._application.get_definition().get_arguments())
            self._definition.add_arguments(current_arguments)

        self._definition.add_options(self._application.get_definition().get_options())

        self._application_definition_merged = True
        if merge_args:
            self._application_definition_merged_with_args = True

    def set_definition(self, definition):
        if isinstance(definition, InputDefinition):
            self._definition = definition
        else:
            self._definition.set_definition(definition)

        self._application_definition_merged = False

        return self

    def get_definition(self):
        return self._definition

    def get_native_definition(self):
        return self.get_definition()

    def add_argument(self, name, mode=None, description='', default=None):
        self._definition.add_argument(InputArgument(name, mode, description, default))

        return self

    def add_argument_from_dict(self, argument_dict):
        argument = InputArgument.from_dict(argument_dict)

        self._definition.add_argument(argument)

        return self

    def add_option(self, name, shortcut=None, mode=None, description='', default=None):
        self._definition.add_option(InputOption(name, shortcut, mode, description, default))

        return self

    def add_option_from_dict(self, option_dict):
        option = InputOption.from_dict(option_dict)

        self._definition.add_option(option)

        return self

    def set_name(self, name):
        self.validate_name(name)

        self._name = name

        return self

    def get_name(self):
        return self._name

    def set_description(self, description):
        self._description = description

        return self

    def get_description(self):
        return self._description

    def set_help(self, help_):
        self._help = help_

        return self

    def get_help(self):
        return self._help

    def set_aliases(self, aliases):
        for alias in aliases:
            self.validate_name(alias)

        self._aliases = aliases

        return self

    def get_aliases(self):
        return self._aliases

    def get_synopsis(self):
        if self._synopsis is None:
            self._synopsis = (
                '%s %s'
                % (self._name,
                   self._definition.get_synopsis())
            ).strip()

        return self._synopsis

    def get_helper(self, name):
        return self._helper_set.get(name)

    def get_processed_help(self):
        name = self._name

        h = self.get_help()

        h = h.replace('%command.full_name%', name)
        h = h.replace('%command.name%', name)

        return h

    def as_text(self):
        if self._application and not self._application_definition_merged:
            self.get_synopsis()
            self.merge_application_definition(False)

        messages = [
            '<comment>Usage:</comment>',
            ' ' + self.get_synopsis(),
            '',
        ]

        if self.get_aliases():
            messages.append('<comment>Aliases:</comment> <info>' + ', '.join(self.get_aliases()) + '</info>')

        messages.append(self.get_native_definition().as_text())

        h = self.get_processed_help()
        if h:
            messages.append('<comment>Help:</comment>')
            messages.append(' ' + h.replace('\n', '\n ') + '\n')

        return '\n'.join(messages)

    def validate_name(self, name):
        if not re.match('^[^:]+(:[^:]+)*$', name):
            raise CommandError('Command name "%s" is invalid.' % name)

    @classmethod
    def from_dict(cls, command_dict):
        """
        Creates a command from a dictionary.

        @param command_dict: The dictionary defining the commmand
        @type command_dict: dict

        @return: The command
        @rtype: Command
        """
        if len(command_dict) > 1:
            raise Exception('Only one command can be defined (%d given).'
                            % len(command_dict))

        name = list(command_dict.keys())[0]
        command = Command(name)

        command_dict = command_dict[name]

        if 'description' in command_dict:
            command.set_description(command_dict['description'])

        if 'aliases' in command_dict:
            command.set_aliases(command_dict['aliases'])

        if 'code' in command_dict:
            command.set_code(command_dict['code'])

        for argument in command_dict.get('arguments', []):
            command.add_argument_from_dict(argument)

        for option in command_dict.get('options', []):
            command.add_option_from_dict(option)

        return command
