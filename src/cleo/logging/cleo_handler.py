from __future__ import annotations

import logging

from typing import TYPE_CHECKING
from typing import ClassVar

from cleo.io.outputs.output import Verbosity


if TYPE_CHECKING:
    from cleo.io.outputs.output import Output


class CleoHandler(logging.Handler):
    """
    A handler class which writes logging records, appropriately formatted,
    to a Cleo output stream.
    """

    tags: ClassVar[dict[str, str]] = {
        "CRITICAL": "<error>",
        "ERROR": "<error>",
        "WARNING": "<fg=yellow>",
        "DEBUG": "<fg=dark_gray>",
    }

    def __init__(self, output: Output):
        super().__init__()
        self.output = output

    def emit(self, record: logging.LogRecord) -> None:
        """
        Emit a record.

        If a formatter is specified, it is used to format the record.
        The record is then written to the output with a trailing newline.  If
        exception information is present, it is formatted using
        traceback.print_exception and appended to the stream.  If the stream
        has an 'encoding' attribute, it is used to determine how to do the
        output to the stream.
        """
        try:
            msg = self.tags.get(record.levelname, "") + self.format(record) + "</>"
            self.output.write(msg, new_line=True)

        except Exception:
            self.handleError(record)

    def setLevel(self, verbosity: Verbosity) -> None:  # noqa: N802
        """
        Set the logging level of this handler. verbosity must be an instance of Cleo's Verbosity enum.
        This level is then mapped to it's corresponding `logging` level.
        """
        level_mapping = {
            Verbosity.QUIET: logging.CRITICAL,  # Nothing gets emitted to the output anyway
            Verbosity.NORMAL: logging.WARNING,
            Verbosity.VERBOSE: logging.INFO,
            Verbosity.VERY_VERBOSE: logging.DEBUG,
            Verbosity.DEBUG: logging.DEBUG,
        }
        return super().setLevel(level_mapping[verbosity])
