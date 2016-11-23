# -*- coding: utf-8 -*-

from collections import OrderedDict


class ApplicationDescription(object):

    GLOBAL_NAMESPACE = '_global'

    def __init__(self, application, namespace=None):
        """
        Constructor.

        :type application: Application
        :type namespace: str
        """
        self._application = application
        self._namespace = namespace
        self._namespaces = OrderedDict()
        self._commands = OrderedDict()
        self._aliases = {}

        self._inspect_application()

    def get_namespaces(self):
        return self._namespaces

    def get_commands(self):
        return self._commands

    def get_command(self, name):
        if name not in self._commands and name not in self._aliases:
            raise ValueError('Command %s does not exist.' % name)

        return self._commands.get(name, self._aliases.get(name))

    def _inspect_application(self):
        namespace = None
        if self._namespace:
            namespace = self._application.find_namespace(self._namespace)

        all = self._application.all(namespace)

        for namespace, commands in self._sort_commands(all):
            names = []

            for name, command in commands:
                if not command.get_name() or command.is_hidden():
                    continue

                if command.get_name() == name:
                    self._commands[name] = command
                else:
                    self._aliases[name] = command

                names.append(name)

            self._namespaces[namespace] = {'id': namespace, 'commands': names}

    def _sort_commands(self, commands):
        """
        Sorts command in alphabetical order

        :param commands: A dict of commands
        :type commands: dict

        :return: A sorted list of commands
        """
        namespaced_commands = {}
        for name, command in commands.items():
            key = self._application.extract_namespace(name, 1)
            if not key:
                key = '_global'

            if key in namespaced_commands:
                namespaced_commands[key][name] = command
            else:
                namespaced_commands[key] = {name: command}

        for namespace, commands in namespaced_commands.items():
            namespaced_commands[namespace] = sorted(commands.items(), key=lambda x: x[0])

        namespaced_commands = sorted(namespaced_commands.items(), key=lambda x: x[0])

        return namespaced_commands

