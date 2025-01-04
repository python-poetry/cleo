from __future__ import annotations

import logging

from typing import ClassVar

from cleo.commands.command import Command


_logger = logging.getLogger(__file__)


def log_stuff() -> None:
    _logger.debug("This is an debug log record")
    _logger.info("This is an info log record")
    _logger.warning("This is an warning log record")
    _logger.error("This is an error log record")


class Foo4Command(Command):
    name = "foo4"

    description = "The foo4 bar command"

    aliases: ClassVar[list[str]] = ["foo4"]

    def handle(self) -> int:
        log_stuff()
        return 0
