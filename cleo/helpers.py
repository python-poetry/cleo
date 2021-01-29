from typing import Any
from typing import Optional

from cleo.io.inputs.argument import Argument
from cleo.io.inputs.option import Option


def argument(
    name: str,
    description: Optional[str] = None,
    optional: bool = False,
    multiple: bool = False,
    default: Optional[Any] = None,
) -> Argument:
    return Argument(
        name,
        required=not optional,
        is_list=multiple,
        description=description,
        default=default,
    )


def option(
    long_name: str,
    short_name: Optional[str] = None,
    description: Optional[str] = None,
    flag: bool = True,
    value_required: bool = True,
    multiple: bool = False,
    default: Optional[Any] = None,
) -> Option:
    return Option(
        long_name,
        short_name,
        flag=flag,
        requires_value=value_required,
        is_list=multiple,
        description=description,
        default=default,
    )
