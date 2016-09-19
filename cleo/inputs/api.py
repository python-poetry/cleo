# -*- coding: utf-8 -*-

from .input_argument import InputArgument
from .input_option import InputOption


def argument(name, description='',
             required=False, default=None, is_list=False,
             validator=None):
    """
    Helper function to create a new argument.

    :param name: The name of the argument.
    :type name: str

    :param description: A helpful description of the argument.
    :type description: str

    :param required: Whether the argument is required or not.
    :type required: bool

    :param default: The default value of the argument.
    :type default: mixed

    :param is_list: Whether the argument should be a list or not.
    :type list: bool

    :param validator: An optional validator.
    :type validator: Validator or str

    :rtype: InputArgument
    """
    mode = InputArgument.OPTIONAL
    if required:
        mode = InputArgument.REQUIRED

    if is_list:
        mode |= InputArgument.IS_LIST

    return InputArgument(name, mode, description, default, validator)


def option(name, shortcut=None, description='',
           flag=True, value_required=None, is_list=False,
           default=None, validator=None):
    """
    Helper function to create an option.

    :param name: The name of the option
    :type name: str

    :param shortcut: The shortcut (Optional)
    :type shortcut: str or None

    :param description: The description of the option.
    :type description: str

    :param flag: Whether the option is a flag or not.
    :type flag: bool

    :param value_required: Whether a value is required or not.
    :type value_required: bool or None

    :param is_list: Whether the option is a list or not.
    :type is_list: bool

    :param default: The default value.
    :type default: mixed

    :param validator: An optional validator.
    :type validator: Validator or str

    :rtype: InputOption
    """
    mode = InputOption.VALUE_IS_FLAG

    if value_required is True:
        mode = InputOption.VALUE_REQUIRED
    elif value_required is False:
        mode = InputOption.VALUE_OPTIONAL

    if is_list:
        mode |= InputOption.VALUE_IS_LIST

    return InputOption(
        name, shortcut, mode, description,
        default, validator
    )

