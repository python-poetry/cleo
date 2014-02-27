# -*- coding: utf-8 -*-

try:
    import ujson as json
except ImportError:
    import json

from collections import OrderedDict

from .input_option import InputOption


class InputDefinition(object):

    def __init__(self, definition=None):
        definition = definition or []

        self.set_definition(definition)

    def set_definition(self, definition):
        arguments = []
        options = []
        for item in definition:
            if isinstance(item, InputOption):
                options.append(item)
            else:
                arguments.append(item)

        self.set_arguments(arguments)
        self.set_options(options)

    def set_arguments(self, arguments=None):
        arguments = arguments or []

        self.__arguments = OrderedDict()
        self.__required_count = 0
        self.__has_an_array_argument = False
        self.__has_optional = False

        self.add_arguments(arguments)

    def add_arguments(self, arguments=None):
        arguments = arguments or []

        for argument in arguments:
            self.add_argument(argument)

    def add_argument(self, argument):
        if argument.get_name() in self.__arguments:
            raise Exception('An argument with name "%s" already exists.' % argument.get_name())

        if self.__has_an_array_argument:
            raise Exception('Cannot add an argument after a list argument.')

        if argument.is_required() and self.__has_optional:
            raise Exception('Cannot add a required argument after an optional one.')

        if argument.is_list():
            self.__has_an_array_argument = True

        if argument.is_required():
            self.__required_count += 1
        else:
            self.__has_optional = True

        self.__arguments[argument.get_name()] = argument

    def get_argument(self, name):
        arguments = list(self.__arguments.values()) if isinstance(name, int) else self.__arguments

        if not self.has_argument(name):
            raise Exception('The "%s" argument does not exist.' % name)

        return arguments[name]

    def has_argument(self, name):
        arguments = list(self.__arguments.values()) if isinstance(name, int) else self.__arguments

        try:
            arguments[name]

            return True
        except (KeyError, IndexError):
            return False

    def get_arguments(self):
        """
        Gets the list of InputArguments objects.

        @return: A list of InputArguments objects
        @rtype: list
        """
        return list(self.__arguments.values())

    def get_argument_count(self):
        return len(self.__arguments) if not self.__has_an_array_argument else 10000000

    def get_argument_required_count(self):
        return self.__required_count

    def get_argument_defaults(self):
        values = {}

        for argument in self.__arguments.values():
            if not argument.is_required():
                values[argument.get_name()] = argument.get_default()

        return values

    def set_options(self, options=None):
        options = options or []

        self.__options = OrderedDict()
        self.__shortcuts = OrderedDict()

        self.add_options(options)

    def add_options(self, options=None):
        options = options or []

        for option in options:
            self.add_option(option)

    def add_option(self, option):
        if option.get_name() in self.__options \
                and not option.equals(self.__options[option.get_name()]):
            raise Exception('An option named "%s" already exists.' % option.get_name())
        elif option.get_shortcut() in self.__shortcuts \
                and not option.equals(self.__options[self.__shortcuts[option.get_shortcut()]]):
            raise Exception('An option with shortcut "%s" already exists.' % option.get_shortcut())

        self.__options[option.get_name()] = option
        if option.get_shortcut():
            for shortcut in option.get_shortcut().split('|'):
                self.__shortcuts[shortcut] = option.get_name()

    def get_option(self, name):
        if not self.has_option(name):
            raise Exception('The "--%s" option does not exist.' % name)

        return self.__options[name]

    def has_option(self, name):
        return name in self.__options

    def get_options(self):
        return list(self.__options.values())

    def has_shortcut(self, name):
        return name in self.__shortcuts

    def get_option_for_shortcut(self, shortcut):
        return self.get_option(self.shortcut_to_name(shortcut))

    def get_option_defaults(self):
        values = {}
        for option in self.__options.values():
            values[option.get_name()] = option.get_default()

        return values

    def shortcut_to_name(self, shortcut):
        if not self.has_shortcut(shortcut):
            raise Exception('The "-%s" option does not exist.' % shortcut)

        return self.__shortcuts[shortcut]

    def get_synopsis(self):
        elements = []
        for option in self.get_options():
            shortcut = '-%s|' % option.get_shortcut() if option.get_shortcut() else ''

            if option.is_value_required():
                element = '%s--%s="..."'
            elif option.is_value_optional():
                element = '%s--%s[="..."]'
            else:
                element = '%s--%s'

            elements.append('[%s]' % (element % (shortcut, option.get_name())))

        for argument in self.get_arguments():
            if argument.is_required():
                element = '%s'
            else:
                element = '[%s]'

            elements.append(element % (argument.get_name() + ('1' if argument.is_list() else '')))
            if argument.is_list():
                elements.append('... [%sN]' % argument.get_name())

        return ' '.join(elements)

    def as_text(self):
        # find the largest option or argument name
        mx = 0
        for option in self.get_options():
            name_length = len(option.get_name()) + 2
            if option.get_shortcut():
                name_length += len(option.get_shortcut()) + 3

            mx = max(mx, name_length)

        for argument in self.get_arguments():
            mx = max(mx, len(argument.get_name()))
        mx += 1

        text = []

        if self.get_arguments():
            text.append('<comment>Arguments:</comment>')
            for argument in self.get_arguments():
                if argument.get_default() is not None\
                    and (not isinstance(argument.get_default(), list)
                         or len(argument.get_default())):
                    default = '<comment> (default: %s)</comment>' % self.format_default_value(argument.get_default())
                else:
                    default = ''

                description = argument.get_description().replace('\n', '\n' + ' ' * (mx + 2))

                text.append(' <info>%-*s</info> %s%s' % (mx, argument.get_name(), description, default))

            text.append('')

        if self.get_options():
            text.append('<comment>Options:</comment>')
            for option in self.get_options():
                if option.accept_value() \
                    and option.get_default() is not None \
                    and (not isinstance(option.get_default(), list)
                         or len(option.get_default())):
                    default = '<comment> (default: %s)</comment>' % self.format_default_value(option.get_default())
                else:
                    default = ''

                multiple = '<comment> (multiple values allowed)</comment>' if option.is_list() else ''
                description = option.get_description().replace('\n', '\n' + ' ' * (mx + 2))

                option_max = mx - len(option.get_name()) - 2
                text.append(' <info>%s</info> %-*s%s%s%s'
                            % ('--' + option.get_name(),
                               option_max,
                               '(-%s) ' % option.get_shortcut() if option.get_shortcut() else '',
                               description,
                               default,
                               multiple))

            text.append('')

        return '\n'.join(text)

    def format_default_value(self, default):
        return json.dumps(default)
