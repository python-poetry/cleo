# -*- coding: utf-8 -*-


class InputArgument(object):
    """
    Represents a command line argument.
    """

    REQUIRED = 1
    OPTIONAL = 2
    IS_LIST = 4

    def __init__(self, name, mode=None, description='', default=None):
        """
        Constructor

        @param name: The argument name
        @type name: str
        @param mode: The argument mode: REQUIRED or OPTIONAL
        @type mode: int or None
        @param description: A description text
        @type description: str
        @param default: The default value (for OPTIONAL mode only)
        @type default: mixed
        """
        if mode is None:
            mode = self.__class__.OPTIONAL
        elif not isinstance(mode, int) or mode > 7 or mode < 1:
            raise Exception('Argument mode "%s" is not valid.' % mode)

        self.__name = name
        self.__mode = mode
        self.__description = description

        self.set_default(default)

    def get_name(self):
        """
        Returns the argument name

        @return: The argument name
        @rtype: str
        """
        return self.__name

    def is_required(self):
        """
        Returns True if the argument is required.

        @return: True if parameter mode is REQUIRED, False otherwise
        @rtype: bool
        """
        return self.__class__.REQUIRED == (self.__class__.REQUIRED & self.__mode)

    def is_list(self):
        """
        Returns True if the argument can take multiple values

        @return: True if mode is IS_LIST, False otherwise
        @rtype: bool
        """
        return self.__class__.IS_LIST == (self.__class__.IS_LIST & self.__mode)

    def set_default(self, default=None):
        """
        Sets the default value.

        @param default: The default value
        @type default: mixed
        """
        if self.is_required() and default is not None:
            raise Exception('Cannot set a default value except for InputArgument::OPTIONAL mode.')

        if self.is_list():
            if default is None:
                default = []
            elif not isinstance(default, list):
                raise Exception('A default value for an array argument must be an array.')

        self.__default = default

    def get_default(self):
        """
        Returns the default value.

        @return: The default value
        @rtype: mixed
        """
        return self.__default

    def get_description(self):
        """
        Returns the description text.

        @return: The description text
        @rtype: str
        """
        return self.__description
