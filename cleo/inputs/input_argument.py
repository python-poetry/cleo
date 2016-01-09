# -*- coding: utf-8 -*-

from ..validators import ValidationError, VALIDATORS


class InvalidArgument(ValidationError):

    def __init__(self, argument, msg, value=ValidationError._UNDEFINED):
        self.argument = argument
        self.msg = msg
        self.value = value

        super(ValidationError, self).__init__(str(self))

    def to_s(self):
        if self.value != self._UNDEFINED:
            return 'Invalid value %s (%s) ' \
                   'for argument %s: %s'\
                   % (repr(self.value),
                      self.value.__class__.__name__,
                      self.argument.get_name(),
                      self.msg)

        return self.msg


class InputArgument(object):
    """
    Represents a command line argument.
    """

    REQUIRED = 1
    OPTIONAL = 2
    IS_LIST = 4

    def __init__(self, name, mode=None,
                 description='', default=None, validator=None):
        """
        Constructor

        :param name: The argument name
        :type name: str
        :param mode: The argument mode: REQUIRED or OPTIONAL
        :type mode: int or None
        :param description: A description text
        :type description: str
        :param default: The default value (for OPTIONAL mode only)
        :type default: mixed
        :param validator: A Validator instance or a callable
        :type validator: Validator or callable
        """
        if mode is None:
            mode = self.OPTIONAL
        elif not isinstance(mode, int) or mode > 7 or mode < 1:
            raise Exception('Argument mode "%s" is not valid.' % mode)

        self.__name = name
        self.__mode = mode
        self.__description = description or ''
        self.__validator = VALIDATORS.get(validator)

        self.set_default(default)

    def get_name(self):
        """
        Returns the argument name

        :return: The argument name
        :rtype: str
        """
        return self.__name

    def is_required(self):
        """
        Returns True if the argument is required.

        :return: True if parameter mode is REQUIRED, False otherwise
        :rtype: bool
        """
        return self.__class__.REQUIRED == (self.__class__.REQUIRED & self.__mode)

    def is_list(self):
        """
        Returns True if the argument can take multiple values

        :return: True if mode is IS_LIST, False otherwise
        :rtype: bool
        """
        return self.__class__.IS_LIST == (self.__class__.IS_LIST & self.__mode)

    def set_default(self, default=None):
        """
        Sets the default value.

        :param default: The default value
        :type default: mixed
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

        :return: The default value
        :rtype: mixed
        """
        return self.__default

    def get_description(self):
        """
        Returns the description text.

        :return: The description text
        :rtype: str
        """
        return self.__description

    def get_validator(self):
        """
        Returns the validator

        :return: The validator
        :rtype: Validator or callable
        """
        return self.__validator

    def set_validator(self, validator):
        """
        Sets the valdidator.

        :param validator: A Validator instance
        :type validator: Validator
        """
        self.__validator = VALIDATORS.get(validator)

        return self

    @classmethod
    def from_dict(cls, argument_dict):
        """
        Created a InputArgument instance from a dictionary.

        :param argument_dict: The dictionary defining the argument
        :type argument_dict: dict

        :return: The created InputArgument instance
        :rtype: InputArgument
        """
        if len(argument_dict) > 1:
            name = argument_dict['name']
        else:
            name = list(argument_dict.keys())[0]
            argument_dict = argument_dict[name]

        description = argument_dict.get('description')
        default = argument_dict.get('default')
        required = argument_dict.get('required', False)
        mode = cls.REQUIRED if required else cls.OPTIONAL

        if argument_dict.get('list', False):
            mode |= cls.IS_LIST

        validator = argument_dict.get('validator')

        return cls(name, mode, description, default, validator=validator)
