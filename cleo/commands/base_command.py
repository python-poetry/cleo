# -*- coding: utf-8 -*-

import os
import sys
import re
import copy
import inspect

from ..inputs.input import Input
from ..inputs.input_definition import InputDefinition
from ..inputs.input_argument import InputArgument
from ..inputs.input_option import InputOption
from ..outputs.output import Output


class CommandError(Exception):
    pass


class BaseCommand(object):

    def __init__(self, name=None):
        self._definition = InputDefinition()
        self._ignore_validation_errors = False
        self._application_definition_merged = False
        self._application_definition_merged_with_args = False
        self._application = None
        self._helper_set = None
        self._usages = []
        self._synopsis = {}
        self._code = None

        if hasattr(self, 'aliases'):
            self.set_aliases(self.aliases)
        else:
            self.aliases = []

        if hasattr(self, 'help'):
            self.set_help(self.help)
        else:
            self.help = ''

        self.name = name or getattr(self, 'name', None)

        if hasattr(self, 'description'):
            self.set_description(self.description)
        else:
            self.description = ''

        if hasattr(self, 'usages'):
            for usage in copy.copy(self.usages):
                self.add_usage(usage)
        else:
            self._usages = []

        if name is not None:
            self.set_name(name)

        self.configure()

        if not self.name:
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
        if hasattr(self, 'arguments'):
            for argument in self.arguments:
                if isinstance(argument, InputArgument):
                    self._definition.add_argument(argument)
                else:
                    raise Exception('Invalid argument')

        if hasattr(self, 'options'):
            for option in self.options:
                if isinstance(option, InputOption):
                    self._definition.add_option(option)
                else:
                    raise Exception('Invalid option')

    def execute(self, input_, output_):
        raise NotImplementedError()

    def interact(self, input_, output_):
        pass

    def initialize(self, input_, output_):
        pass

    def run(self, input_, output_):
        """
        Runs the command.

        :param input_: an Input instance
        :type input_: Input
        :param output_: an Output instance
        :type output_: Output

        :return: The command exit code
        :rtype: int
        """
        # force the creation of the synopsis before the merge with the app definition
        self.get_synopsis(True)
        self.get_synopsis(False)

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
            status_code = self._execute_code(input_, output_)
        else:
            status_code = self.execute(input_, output_)

        try:
            return int(float(status_code))
        except (TypeError, ValueError):
            return 0

    def _execute_code(self, input_, output):
        return self._code(input_, output)

    def set_code(self, code):
        if not callable(code):
            raise Exception('Invalid callable provided to Command.setCode().')

        self._code = code

        return self

    def merge_application_definition(self, merge_args=True):
        """
        Merges the application definition with the command definition.

        This method should not be used directly.

        :param merge_args: Whether to merge or not the Application definition arguments to Command definition arguments
        :type merge_args: bool
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

    def add_argument(self, name, mode=None,
                     description='', default=None, validator=None):
        self._definition.add_argument(
            InputArgument(name, mode, description, default, validator)
        )

        return self

    def add_option(self, name, shortcut=None, mode=None,
                   description='', default=None, validator=None):
        self._definition.add_option(
            InputOption(name, shortcut, mode, description, default, validator)
        )

        return self

    def set_name(self, name):
        self.validate_name(name)

        self.name = name

        return self

    def get_name(self):
        return self.name

    def set_description(self, description):
        self.description = description

        return self

    def get_description(self):
        return self.description

    def set_help(self, help_):
        self.help = help_

        return self

    def get_help(self):
        return self.help

    def set_aliases(self, aliases):
        for alias in aliases:
            self.validate_name(alias)

        self.aliases = aliases

        return self

    def get_aliases(self):
        return self.aliases

    def add_usage(self, usage):
        if usage.find(self.name) != 0:
            usage = '%s %s' % (self.name, usage)

        self._usages.append(usage)

        return self

    def get_usages(self):
        return self._usages

    def get_synopsis(self, short=False):
        key = 'long'
        if short:
            key = 'short'

        if key not in self._synopsis:
            self._synopsis[key] = (
                '%s %s'
                % (self.name,
                   self._definition.get_synopsis(short))
            ).strip()

        return self._synopsis[key]

    def get_helper(self, name):
        return self._helper_set.get(name)

    def get_processed_help(self):
        name = self.name

        h = self.get_help() or self.get_description()

        h = h.replace('%script.full_name%', self._get_script_full_name())
        h = h.replace('%script.name%', self._get_script_name())

        h = h.replace('%command.full_name%', self._get_command_full_name())
        h = h.replace('%command.name%', name)

        return h

    def _get_command_full_name(self):
        return inspect.stack()[-1][1] + ' ' + self.name

    def _get_script_full_name(self):
        return os.path.realpath(sys.argv[0])

    def _get_script_name(self):
        return os.path.basename(self._get_script_full_name())

    def validate_name(self, name):
        if not re.match('^[^:]+(:[^:]+)*$', name):
            raise CommandError('Command name "%s" is invalid.' % name)
