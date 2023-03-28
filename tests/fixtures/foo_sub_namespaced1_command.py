from __future__ import annotations

from cleo.commands.command import Command


class FooSubNamespaced1Command(Command):
    name = "foo bar baz"

    description = "The foo bar baz command"

    aliases = ["foobarbaz"]

    def handle(self) -> int:
        return 0
