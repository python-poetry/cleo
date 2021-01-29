from typing import List
from typing import Optional

from cleo._utils import find_similar_names


class CleoException(Exception):

    exit_code: Optional[int] = None


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
    def __init__(self, name: str, commands: Optional[List[str]] = None) -> None:
        message = 'The command "{}" does not exist.'.format(name)

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
    def __init__(self, name: str, namespaces: Optional[List[str]] = None) -> None:
        message = 'There are no commands in the "{}" namespace.'.format(name)

        if namespaces:
            suggested_names = find_similar_names(name, namespaces)

            if suggested_names:
                if len(suggested_names) == 1:
                    message += "\n\nDid you mean this?\n    "
                else:
                    message += "\n\nDid you mean one of these?\n    "

                message += "\n    ".join(suggested_names)

        super().__init__(message)
