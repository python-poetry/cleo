from typing import Any
from typing import Optional

from clikit.api.args.format import Argument
from clikit.api.args.format import Option


def argument(
    name, description=None, optional=False, multiple=False, default=None
):  # type: (str, Optional[str], bool, bool, Optional[Any]) -> Argument
    if optional:
        flags = Argument.OPTIONAL
    else:
        flags = Argument.REQUIRED

    if multiple:
        flags |= Argument.MULTI_VALUED

    return Argument(name, flags, description, default)


def option(
    long_name,
    short_name=None,
    description=None,
    flag=True,
    value_required=True,
    multiple=False,
    default=None,
):  # type: (str, Optional[str], Optional[str], bool, bool, bool, Optional[Any]) -> Option
    if flag:
        flags = Option.NO_VALUE
    elif value_required:
        flags = Option.REQUIRED_VALUE
    else:
        flags = Option.OPTIONAL_VALUE

    if multiple and not flag:
        flags |= Option.MULTI_VALUED

    return Option(long_name, short_name, flags, description, default)
