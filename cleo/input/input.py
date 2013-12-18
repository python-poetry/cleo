# -*- coding: utf-8 -*-

from .input_definition import InputDefinition


class Input(object):

    interactive = True

    def __init__(self, definition=None):
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

    def parse(self):
        raise NotImplementedError()

    def validate(self):
        if len(self.get_arguments()) < self.definition.get_argument_required_count():
            raise Exception('Not enough arguments')

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
            raise Exception('Option "%s" does not exist' % name)

        return self.options.get(name, self.definition.get_option(name).get_default())

    def set_option(self, name, value):
        if not self.definition.has_option(name):
            raise Exception('Argument "%s" does not exist')

        self.options[name] = value

    def has_option(self, name):
        return self.definition.has_option(name)
