# -*- coding: utf-8 -*-

from .input import Input


class ListInput(Input):
    """
    ListInput represents an input provided as an array.

    Usage:
    >>> input_ = ListInput([('name', 'foo'), ('--bar', 'foobar')])
    """
    def __init__(self, parameters, definition=None):
        """
        Constructor

        :param parameters: A dict of parameters
        :type parameters: list
        :param definition: An InputDefinition instance
        :type definition: InputDefinition
        """
        self.interactive = False
        self.parameters = parameters

        super(ListInput, self).__init__(definition)

    def get_first_argument(self):
        """
        Returns the first argument from the raw parameters (not parsed)

        :return: The value of the first argument or None otherwise
        :rtype: str
        """
        for item in self.parameters:
            if isinstance(item, tuple):
                key = item[0]
                value = item[1]
            else:
                key = item
                value = item

            if key and '-' == key[0]:
                continue

            return value

    def has_parameter_option(self, values):
        """
        Returns true if the raw parameters (not parsed) contain a value.

        This method is to be used to introspect the input parameters
        before they have been validated. It must be used carefully.

        :param values: The values to look for in the raw parameters (can be a list)
        :type values: str or list

        :return: True if the value is contained in the raw parameters
        :rtype: bool
        """
        if not isinstance(values, list):
            values = [values]

        for item in self.parameters:
            if isinstance(item, tuple):
                key = item[0]
            else:
                key = item

            if key in values:
                return True

        return False

    def get_parameter_option(self, values, default=False):
        """
        Returns the value of a raw option (not parsed).

        This method is to be used to introspect the input parameters
        before they have been validated. It must be used carefully.

        :param values: The values to look for in the raw parameters (can be a list)
        :type values: str or list
        :param default: The default value to return if no result is found
        :type default: mixed

        :return: The option value
        :rtype: mixed
        """
        if not isinstance(values, list):
            values = [values]

        for item in self.parameters:
            if isinstance(item, tuple):
                key = item[0]
                value = item[1]
            else:
                key = item
                value = None

            if key in values:
                return value

        return default

    def parse(self):
        """
        Processes command line arguments.
        """
        for item in self.parameters:
            if isinstance(item, tuple):
                key = item[0]
                value = item[1]
            else:
                key = item
                value = None

            if key.startswith('--'):
                self.add_long_option(key[2:], value)
            elif key[0] == '-':
                self.add_short_option(key[1:], value)
            else:
                self.add_argument(key, value)

    def add_short_option(self, shortcut, value):
        """
        Adds a short option value

        :param shortcut: The short option key
        :type shortcut: str
        :param value: The value for the option
        :type value: mixed
        """
        if not self.definition.has_shortcut(shortcut):
            raise Exception('The "-%s" option does not exist.' % shortcut)

        self.add_long_option(self.definition.get_option_for_shortcut(shortcut).get_name(), value)

    def add_long_option(self, name, value):
        """
        Adds a long option value

        :param name: The long option key
        :type name: str
        :param value: The value for the option
        :type value: mixed
        """
        if not self.definition.has_option(name):
            raise Exception('The "--%s" option does not exist.' % name)

        option = self.definition.get_option(name)

        if value is None:
            if option.is_value_required():
                raise Exception('The "--%s" option requires a value.' % name)

            value = option.get_default() if option.is_value_optional() else True

        self.options[name] = value

    def add_argument(self, name, value):
        """
        Adds an argument value

        :param name: The argument key
        :type name: str
        :param value: The value for the argument
        :type value: mixed
        """
        if not self.definition.has_argument(name):
            raise Exception('The "%s" argument does not exist.' % name)

        self.arguments[name] = value
