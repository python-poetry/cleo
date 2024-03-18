from __future__ import annotations

from enum import Enum


SUPPRESS = "==SUPPRESS=="
_UNRECOGNIZED_ARGS_ATTR = "_unrecognized_args"


class NArgsEnum(str, Enum):
    OPTIONAL = "?"
    ZERO_OR_MORE = "*"
    ONE_OR_MORE = "+"
    PARSER = "A..."
    REMAINDER = "..."


def _copy_items(items):
    if items is None:
        return []
    # The copy module is used only in the 'append' and 'append_const'
    # actions, and it is needed only when the default value isn't a list.
    # Delay its import for speeding up the common case.
    if isinstance(items, list):
        return items[:]
    import copy

    return copy.copy(items)
