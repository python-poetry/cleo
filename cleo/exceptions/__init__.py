from __future__ import annotations

from typing import List
from typing import Optional

from cleo._utils import find_similar_names


class CleoException(Exception):

    exit_code: int | None = None


class CleoSimpleException(Exception):

    pass


class LogicException(CleoException):

    pass


class RuntimeException(CleoException):

    pass


class ValueException(CleoException):

    pass


class MissingArgumentsException(CleoSimpleException):

    pass


class NoSuchOptionException(CleoException):

    pass


class CommandNotFoundException(CleoSimpleException):
    def __init__(self, name: str, commands: list[str] | None = None) -> None:
        message = f'The command "{name}" does not exist.'

        if commands:
            suggested_names = find_similar_names(name, commands)

            if suggested_names:
                if len(suggested_names) == 1:
                    message += "\n\nDid you mean this?\n    "
                else:
                    message += "\n\nDid you mean one of these?\n    "

                message += "\n    ".join(suggested_names)

        super().__init__(message)


class NamespaceNotFoundException(CleoSimpleException):
    def __init__(self, name: str, namespaces: list[str] | None = None) -> None:
        message = f'There are no commands in the "{name}" namespace.'

        if namespaces:
            suggested_names = find_similar_names(name, namespaces)

            if suggested_names:
                if len(suggested_names) == 1:
                    message += "\n\nDid you mean this?\n    "
                else:
                    message += "\n\nDid you mean one of these?\n    "

                message += "\n    ".join(suggested_names)

        super().__init__(message)
