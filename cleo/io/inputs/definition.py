import sys

from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from cleo.exceptions import LogicException

from .argument import Argument
from .option import Option


class Definition:
    """
    A Definition represents a set of command line arguments and options.
    """

    def __init__(
        self, definition: Optional[List[Union[Argument, Option]]] = None
    ) -> None:
        self._arguments: Dict[str, Argument] = {}
        self._required_count = 0
        self._has_a_list_argument = False
        self._has_optional = False
        self._options: Dict[str, Option] = {}
        self._shortcuts: Dict[str, str] = {}

        if definition is None:
            definition = []

        self.set_definition(definition)

    @property
    def arguments(self) -> List[Argument]:
        return list(self._arguments.values())

    @property
    def argument_count(self) -> int:
        if self._has_a_list_argument:
            return sys.maxsize

        return len(self._arguments)

    @property
    def required_argument_count(self) -> int:
        return self._required_count

    @property
    def argument_defaults(self) -> Dict[str, Any]:
        values = {}

        for argument in self._arguments.values():
            values[argument.name] = argument.default

        return values

    @property
    def options(self) -> List[Option]:
        return list(self._options.values())

    @property
    def option_defaults(self) -> Dict[str, Any]:
        values = {}
        for option in self._options.values():
            values[option.name] = option.default

        return values

    def set_definition(self, definition: List[Union[Argument, Option]]) -> None:
        arguments = []
        options = []

        for item in definition:
            if isinstance(item, Option):
                options.append(item)
            else:
                arguments.append(item)

        self.set_arguments(arguments)
        self.set_options(options)

    def set_arguments(self, arguments: List[Argument]) -> None:
        self._arguments = {}
        self._required_count = 0
        self._has_a_list_argument = False
        self._has_optional = False
        self.add_arguments(arguments)

    def add_arguments(self, arguments: List[Argument]) -> None:
        for argument in arguments:
            self.add_argument(argument)

    def add_argument(self, argument: Argument) -> None:
        if argument.name in self._arguments:
            raise LogicException(
                f'An argument with name "{argument.name}" already exists'
            )

        if self._has_a_list_argument:
            raise LogicException("Cannot add an argument after a list argument")

        if argument.is_required() and self._has_optional:
            raise LogicException("Cannot add a required argument after an optional one")

        if argument.is_list():
            self._has_a_list_argument = True

        if argument.is_required():
            self._required_count += 1
        else:
            self._has_optional = True

        self._arguments[argument.name] = argument

    def argument(self, name: Union[str, int]) -> Argument:
        if not self.has_argument(name):
            raise ValueError(f'The "{name}" argument does not exist')

        if isinstance(name, int):
            arguments = list(self._arguments.values())
        else:
            arguments = self._arguments

        return arguments[name]

    def has_argument(self, name: Union[str, int]) -> bool:
        if isinstance(name, int):
            arguments = list(self._arguments.values())
        else:
            arguments = self._arguments

        try:
            arguments[name]
        except (KeyError, IndexError):
            return False

        return True

    def set_options(self, options: List[Option]) -> None:
        self._options = {}
        self._shortcuts = {}
        self.add_options(options)

    def add_options(self, options: List[Option]) -> None:
        for option in options:
            self.add_option(option)

    def add_option(self, option: Option) -> None:
        if option.name in self._options and option != self._options[option.name]:
            raise LogicException(f'An option named "{option.name}" already exists')

        if option.shortcut:
            for shortcut in option.shortcut.split("|"):
                if shortcut in self._shortcuts and option != self._shortcuts[shortcut]:
                    raise LogicException(
                        f'An option with shortcut "{shortcut}" already exists'
                    )

        self._options[option.name] = option

        if option.shortcut:
            for shortcut in option.shortcut.split("|"):
                self._shortcuts[shortcut] = option.name

    def option(self, name: str) -> Option:
        if not self.has_option(name):
            raise ValueError(f'The option "--{name}" option does not exist')

        return self._options[name]

    def has_option(self, name: str) -> bool:
        return name in self._options

    def has_shortcut(self, shortcut: str) -> bool:
        return shortcut in self._shortcuts

    def option_for_shortcut(self, shortcut: str) -> Option:
        return self._options[self.shortcut_to_name(shortcut)]

    def shortcut_to_name(self, shortcut: str) -> str:
        if shortcut not in self._shortcuts:
            raise ValueError(f'The "-{shortcut}" option does not exist')

        return self._shortcuts[shortcut]

    def synopsis(self, short: bool = False) -> str:
        elements = []

        if short and self._options:
            elements.append("[options]")
        elif not short:
            for option in self._options.values():
                value = ""
                if option.accepts_value():
                    value = " {}{}{}".format(
                        "[" if not option.requires_value() else "",
                        option.name.upper(),
                        "]" if not option.requires_value() else "",
                    )

                shortcut = ""
                if option.shortcut:
                    shortcut = "-{}|".format(option.shortcut)

                elements.append("[{}--{}{}]".format(shortcut, option.name, value))

        if elements and self._arguments:
            elements.append("[--]")

        tail = ""
        for argument in self._arguments.values():
            element = f"<{argument.name}>"
            if argument.is_list():
                element += "..."

            if not argument.is_required():
                element = "[" + element
                tail += "]"

            elements.append(element)

        return " ".join(elements) + tail
