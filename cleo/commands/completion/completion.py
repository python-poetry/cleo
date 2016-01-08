# -*- coding: utf-8 -*-


class Completion(object):

    ALL_COMMANDS = None
    ALL_TYPES = None

    TYPE_OPTION = 'option'
    TYPE_ARGUMENT = 'argument'

    def __init__(self, command_name, target_name, type, completion):
        self._command_name = command_name
        self._target_name = target_name
        self._type = type
        self._completion = completion

    def get_command_name(self):
        return self._command_name

    def get_target_name(self):
        return self._target_name

    def get_type(self):
        return self._type

    def run(self):
        if self.is_callable():
            self._completion()

        return self._completion

    def is_callable(self):
        return callable(self._completion)
