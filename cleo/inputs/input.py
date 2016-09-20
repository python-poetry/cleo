# -*- coding: utf-8 -*-

import re
from .input_definition import InputDefinition
from ..validators import ValidationError, Callable, Validator
from .input_argument import InvalidArgument
from .input_option import InvalidOption
from ..exceptions import MissingArguments, NoSuchOption


class Input(object):

    interactive = True

    def __init__(self, definition=None):
        self.interactive = True
        self._stream = None
        if definition is None:
            self.arguments = {}
            self.options = {}
            self.definition = InputDefinition()
        else:
            self.bind(definition)
            self.validate()

    def bind(self, definition):
        self.arguments = {}
        self.options = {}
        self.definition = definition

        self.parse()

    def has_parameter_option(self, values):
        """
        Returns true if the raw parameters (not parsed) contain a value.

        This method is to be used to introspect the input parameters
        before they have been validated. It must be used carefully.

        :param values: The values to look for in the raw parameters (can be a list)
        :type values: str|list
        :return: True if the value is in the raw parameters
        :rtype: bool
        """
        raise NotImplementedError()

    def get_parameter_option(self, values, default=False):
        """
        Returns the value of a raw option (not parsed).

        This method is to be used to introspect the input parameters
        before they have been validated. It must be used carefully.

        :param values: The values to look for in the raw parameters (can be a list)
        :type values: str|list
        :param default: The default value to return if no result is found
        :type default: mixed
        :return: True if the value is in the raw parameters
        :rtype: bool
        """
        raise NotImplementedError()

    def parse(self):
        raise NotImplementedError()

    def validate(self):
        if len(self.get_arguments()) < self.definition.get_argument_required_count():
            raise MissingArguments('Not enough arguments')

        self.validate_arguments()
        self.validate_options()

    def validate_arguments(self):
        """
        Validates the arguments

        :raise: InvalidArgument
        """
        for arg_name, arg_value in self.get_arguments().items():
            arg = self.definition.get_argument(arg_name)
            validator = arg.get_validator()

            if validator:
                if not isinstance(validator, Validator):
                    if callable(validator):
                        validator = Callable(validator)
                    else:
                        raise Exception('Invalid validator specified for argument %s' % arg.name)

                try:
                    validated_value = validator.validate(arg_value)
                    if validated_value is not None:
                        self.arguments[arg_name] = validated_value
                except ValidationError as e:
                    raise InvalidArgument(arg, e.msg, e.value)

    def validate_options(self):
        """
        Validates the options

        :raise: InvalidOptionValue
        """
        for opt_name, opt_value in self.get_options().items():
            opt = self.definition.get_option(opt_name)
            validator = opt.get_validator()

            if validator:
                if not isinstance(validator, Validator):
                    if callable(validator):
                        validator = Callable(validator)
                    else:
                        raise Exception('Invalid validator specified for option %s' % opt.name)

                try:
                    validated_value = validator.validate(opt_value)
                    if validated_value is not None:
                        self.options[opt_name] = validated_value
                except ValidationError as e:
                    raise InvalidOption(opt, e.msg, e.value)

    def is_interactive(self):
        return self.interactive

    def set_interactive(self, interactive):
        self.interactive = interactive

    def get_arguments(self):
        return dict(self.definition.get_argument_defaults(), **self.arguments)

    def get_argument(self, name):
        if not self.definition.has_argument(name):
            raise Exception('Argument "%s" does not exist' % name)

        return self.arguments.get(name, self.definition.get_argument(name).get_default())

    def set_argument(self, name, value):
        if not self.definition.has_argument(name):
            raise Exception('Argument "%s" does not exist')

        self.arguments[name] = value

    def has_argument(self, name):
        return self.definition.has_argument(name)

    def get_options(self):
        return dict(self.definition.get_option_defaults(), **self.options)

    def get_option(self, name):
        if not self.has_option(name):
            raise NoSuchOption('Option "%s" does not exist' % name)

        return self.options.get(name, self.definition.get_option(name).get_default())

    def set_option(self, name, value):
        if not self.definition.has_option(name):
            raise NoSuchOption('Option "%s" does not exist' % name)

        self.options[name] = value

    def has_option(self, name):
        return self.definition.has_option(name)

    def escape_token(self, token):
        if re.match('^[\w-]+$', token):
            return token
        else:
            return "\\'".join("'" + p + "'" for p in token.split("'"))

    def set_stream(self, stream):
        self._stream = stream

    def get_stream(self):
        return self._stream
