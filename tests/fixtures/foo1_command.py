from __future__ import annotations

from typing import ClassVar

from cleo.commands.command import Command


class Foo1Command(Command):
    name = "foo bar1"

    description = "The foo bar1 command"

    aliases: ClassVar[list[str]] = ["afoobar1"]

    def handle(self) -> int:
        return 0
