# -*- coding: utf-8 -*-

import re
from ..validators import ValidationError, VALIDATORS


class InvalidOption(ValidationError):

    def __init__(self, option, msg, value=ValidationError._UNDEFINED):
        self.option = option
        self.msg = msg
        self.value = value

        super(ValidationError, self).__init__(str(self))

    def to_s(self):
        if self.value != self._UNDEFINED:
            return 'Invalid value %s (%s) for option %s: %s'\
                   % (repr(self.value),
                      self.value.__class__.__name__,
                      self.option.get_name(),
                      self.msg)

        return self.msg


class InputOption(object):
    """
    Represents a command line option.
    """

    VALUE_NONE = VALUE_IS_FLAG = 1
    VALUE_REQUIRED = 2
    VALUE_OPTIONAL = 4
    VALUE_IS_LIST = 8

    def __init__(self, name, shortcut=None, mode=None,
                 description='', default=None, validator=None):
        """
        Constructor

        @param name: The option name
        @type name: str
        @param shortcut: The option shortcut
        @type shortcut: str or None or list
        @param mode: The argument mode: VALUE_NONE or VALUE_REQUIRED or VALUE_OPTIONAL
        @type mode: int or None
        @param description: A description text
        @type description: str
        @param default: The default value (must be null for VALUE_REQUIRED or VALUE_NONE)
        @type default: mixed
        @param validator: A Validator instance or a callable
        @type validator: Validator or callable
        """
        if name.startswith('--'):
            name = name[2:]

        if not name:
            raise Exception('An option name cannot be empty.')

        if not shortcut:
            shortcut = None

        if shortcut is not None:
            if isinstance(shortcut, list):
                shortcut = '|'.join(shortcut)

            shortcuts = re.split('\|-?', shortcut.lstrip('-'))
            shortcuts = list(filter(lambda x: x.strip() != '', shortcuts))
            shortcut = '|'.join(shortcuts)

            if not shortcut:
                raise Exception('An option shortcut cannot be empty.')

        if mode is None:
            mode = self.__class__.VALUE_NONE
        elif not isinstance(mode, int) or mode > 15 or mode < 1:
            raise Exception('Option mode "%s" is not valid.' % mode)

        self.__name = name
        self.__shortcut = shortcut
        self.__mode = mode
        self.__description = description
        self.__validator = VALIDATORS.get(validator)

        self.set_default(default)

    def get_shortcut(self):
        """
        Returns the option shortcut.

        @return: The option shortcut
        @rtype: str
        """
        return self.__shortcut

    def get_name(self):
        """
        Returns the option name.

        @return: The option name
        @rtype: str
        """
        return self.__name

    def accept_value(self):
        """
        Returns true if the option accepts a value.

        @return: True if value mode is not VALUE_NONE, False otherwise
        @rtype: bool
        """
        return self.is_value_required() or self.is_value_optional()

    def is_value_required(self):
        """
        Returns True if the option requires a value.

        @return: True if value mode is VALUE_REQUIRED, False otherwise
        """
        return self.__class__.VALUE_REQUIRED == (self.__class__.VALUE_REQUIRED & self.__mode)

    def is_value_optional(self):
        """
        Returns True if the option takes an optional value.

        @return: True if value mode is VALUE_OPTIONAL, False otherwise
        """
        return self.__class__.VALUE_OPTIONAL == (self.__class__.VALUE_OPTIONAL & self.__mode)

    def is_flag(self):
        """
        Returns True if the option is a flag

        @return: True if value mode is VALUE_NONE, False otherwise
        """
        return self.__class__.VALUE_NONE == (self.__class__.VALUE_NONE & self.__mode)

    def is_list(self):
        """
        Returns True if the option can take multiple values

        @return: True if mode is VALUE_IS_LIST, False otherwise
        @rtype: bool
        """
        return self.__class__.VALUE_IS_LIST == (self.__class__.VALUE_IS_LIST & self.__mode)

    def set_default(self, default=None):
        """
        Sets the default value.

        @param default: The default value
        @type default: mixed
        """
        if self.__class__.VALUE_NONE == self.__mode and default is not None:
            raise Exception('Cannot set a default value when using InputOption::VALUE_NONE mode.')

        if self.is_list():
            if default is None:
                default = []
            elif not isinstance(default, list):
                raise Exception('A default value for an array option must be an array.')

        self.__default = default if self.accept_value() else False

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
        @rtype: basestring
        """
        return self.__description

    def get_validator(self):
        """
        Returns the validator

        @return: The validator
        @rtype: Validator or callable
        """
        return self.__validator

    def equals(self, option):
        """
        Checks whether the given option equals this one.

        @param option: option to compare
        @type option: InputOption

        @rtype: bool
        """
        return option.get_name() == self.get_name()\
            and option.get_shortcut() == self.get_shortcut()\
            and option.get_default() == self.get_default()\
            and option.is_list() == self.is_list()\
            and option.is_value_required() == self.is_value_required()\
            and option.is_value_optional() == self.is_value_optional()

    @classmethod
    def from_dict(cls, option_dict):
        """
        Created a InputOption instance from a dictionary.

        @param option_dict: The dictionary defining the argument
        @type option_dict: dict

        @return: The created InputOption instance
        @rtype: InputOption
        """
        if len(option_dict) > 1:
            name = option_dict['name']
        else:
            name = list(option_dict.keys())[0]
            option_dict = option_dict[name]

        description = option_dict.get('description')
        shortcut = option_dict.get('shortcut')
        default = option_dict.get('default')
        value_required = option_dict.get('value_required')
        if value_required is True:
            mode = cls.VALUE_REQUIRED
        elif value_required is False:
            mode = cls.VALUE_OPTIONAL
        else:
            mode = cls.VALUE_NONE

        if option_dict.get('flag') is True:
            mode = cls.VALUE_NONE

        if mode != cls.VALUE_NONE and option_dict.get('list', False):
            mode |= cls.VALUE_IS_LIST

        validator = option_dict.get('validator')

        return cls(name, shortcut, mode, description, default, validator=validator)
