from __future__ import annotations

import logging

from typing import TYPE_CHECKING
from typing import ClassVar

from cleo.commands.command import Command
from cleo.helpers import option


if TYPE_CHECKING:
    from cleo.io.inputs.option import Option


_logger = logging.getLogger(__file__)


def log_stuff() -> None:
    _logger.debug("This is an debug log record")
    _logger.info("This is an info log record")
    _logger.warning("This is an warning log record")
    _logger.error("This is an error log record")


def log_exception() -> None:
    try:
        raise RuntimeError("This is an exception that I raised")
    except RuntimeError as e:
        _logger.exception(e)


class Foo4Command(Command):
    name = "foo4"

    description = "The foo4 bar command"

    aliases: ClassVar[list[str]] = ["foo4"]

    options: ClassVar[list[Option]] = [option("exception")]

    def handle(self) -> int:
        if self.option("exception"):
            log_exception()
        else:
            log_stuff()

        return 0
