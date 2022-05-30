from __future__ import annotations

from typing import Any

from cleo.exceptions import LogicException


class Argument:
    """
    A command line argument.
    """

    def __init__(
        self,
        name: str,
        required: bool = True,
        is_list: bool = False,
        description: str | None = None,
        default: Any | None = None,
    ) -> None:
        self._name = name
        self._required = required
        self._is_list = is_list
        self._description = description
        self._default = None

        self.set_default(default)

    @property
    def name(self) -> str:
        return self._name

    @property
    def default(self) -> str:
        return self._default

    @property
    def description(self) -> str:
        return self._description

    def is_required(self) -> bool:
        return self._required

    def is_list(self) -> bool:
        return self._is_list

    def set_default(self, default: Any | None = None) -> None:
        if self._required and default is not None:
            raise LogicException("Cannot set a default value for required arguments")

        if self._is_list:
            if default is None:
                default = []
            elif not isinstance(default, list):
                raise LogicException(
                    "A default value for a list argument must be a list"
                )

        self._default = default

    def __repr__(self) -> str:
        return (
            "Argument({}, required={}, is_list={}, description={}, default={})".format(
                repr(self._name),
                self._required,
                self._is_list,
                repr(self._description),
                repr(self._default),
            )
        )
