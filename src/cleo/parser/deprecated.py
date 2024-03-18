"""
This module contains parts of parser that should be replaced or removed.
"""

from __future__ import annotations


class _AttributeHolder:
    """Abstract base class that provides __repr__.

    The __repr__ method returns a string in the format::
        ClassName(attr=name, attr=name, ...)
    The attributes are determined either by a class-level attribute,
    '_kwarg_names', or by inspecting the instance __dict__.
    """

    def __repr__(self):
        type_name = type(self).__name__
        arg_strings = [repr(arg) for arg in self._get_args()]
        star_args = {}
        for name, value in self._get_kwargs():
            if name.isidentifier():
                arg_strings.append(f"{name}={value!r}")
            else:
                star_args[name] = value
        if star_args:
            arg_strings.append(f"**{star_args!r}")
        return f'{type_name}({", ".join(arg_strings)})'

    def _get_kwargs(self):
        return list(self.__dict__.items())

    def _get_args(self):
        return []
