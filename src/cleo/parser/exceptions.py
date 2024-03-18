from __future__ import annotations

from cleo.parser.common import SUPPRESS


def _get_action_name(argument):
    if argument is None:
        return None
    if argument.option_strings:
        return "/".join(argument.option_strings)
    if argument.metavar not in (None, SUPPRESS):
        return argument.metavar
    if argument.dest not in (None, SUPPRESS):
        return argument.dest
    if argument.choices:
        return "{" + ",".join(argument.choices) + "}"
    return None


class ArgumentError(Exception):
    """An error from creating or using an argument (optional or positional).

    The string value of this exception is the message, augmented with
    information about the argument that caused it.
    """

    def __init__(self, argument, message):
        self.argument_name = _get_action_name(argument)
        self.message = message

    def __str__(self):
        if self.argument_name is None:
            format = "%(message)s"
        else:
            format = "argument %(argument_name)s: %(message)s"
        return format % {"message": self.message, "argument_name": self.argument_name}


class ArgumentTypeError(Exception):
    """An error from trying to convert a command line string to a type."""
