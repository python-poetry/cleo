from __future__ import annotations

from cleo.commands.command import Command


class Foo1Command(Command):
    name = "foo bar1"

    description = "The foo bar1 command"

    aliases = ["afoobar1"]

    def handle(self) -> int:
        return 0
