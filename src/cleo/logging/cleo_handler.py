from __future__ import annotations

import logging

from logging import LogRecord
from typing import TYPE_CHECKING
from typing import ClassVar
from typing import cast

from cleo.exceptions import CleoUserError
from cleo.io.outputs.output import Verbosity
from cleo.ui.exception_trace.component import ExceptionTrace


if TYPE_CHECKING:
    from cleo.io.outputs.output import Output


class CleoFilter:
    def __init__(self, output: Output):
        self.output = output

    @property
    def current_loglevel(self) -> int:
        verbosity_mapping: dict[Verbosity, int] = {
            Verbosity.QUIET: logging.CRITICAL,  # Nothing gets emitted to the output anyway
            Verbosity.NORMAL: logging.WARNING,
            Verbosity.VERBOSE: logging.INFO,
            Verbosity.VERY_VERBOSE: logging.DEBUG,
            Verbosity.DEBUG: logging.DEBUG,
        }
        return verbosity_mapping[self.output.verbosity]

    def filter(self, record: LogRecord) -> bool:
        return record.levelno >= self.current_loglevel


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
        self.addFilter(CleoFilter(output))

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
            if record.exc_info:
                _type, error, traceback = record.exc_info
                simple = not self.output.is_verbose() or isinstance(
                    error, CleoUserError
                )
                error = cast(Exception, error)
                trace = ExceptionTrace(error)
                trace.render(self.output, simple)

        except Exception:
            self.handleError(record)
