from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar

from cleo.commands.command import Command


if TYPE_CHECKING:
    from cleo.io.io import IO


class FooCommand(Command):
    name = "foo bar"

    description = "The foo bar command"

    aliases: ClassVar[list[str]] = ["afoobar"]

    def interact(self, io: IO) -> None:
        io.write_line("interact called")

    def handle(self) -> int:
        assert self._io is not None
        self._io.write_line("called")

        return 0
