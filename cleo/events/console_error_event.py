from typing import TYPE_CHECKING
from typing import Optional

from cleo.exceptions import CleoException
from cleo.io.io import IO

from .console_event import ConsoleEvent


if TYPE_CHECKING:
    from cleo.commands.command import Command


class ConsoleErrorEvent(ConsoleEvent):
    """
    An event triggered when an exception is raised during the execution of a command.
    """

    def __init__(self, command: Optional["Command"], io: IO, error: Exception) -> None:
        super().__init__(command, io)

        self._error = error
        self._exit_code = None

    @property
    def error(self) -> Exception:
        return self._error

    @property
    def exit_code(self) -> int:
        if self._exit_code is not None:
            return self._exit_code

        if isinstance(self._error, CleoException) and self._error.exit_code is not None:
            return self._error.exit_code

        return 1

    def set_error(self, error: Exception) -> None:
        self._error = error

    def set_exit_code(self, exit_code: int) -> None:
        self._exit_code = exit_code
