from __future__ import annotations

from cleo.commands.command import Command


class Foo2Command(Command):

    name = "foo1 bar"

    description = "The foo1 bar command"

    aliases = ["afoobar2"]

    def handle(self) -> int:
        return 0
