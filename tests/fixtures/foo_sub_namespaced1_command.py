from __future__ import annotations

from typing import ClassVar

from cleo.commands.command import Command


class FooSubNamespaced1Command(Command):
    name = "foo bar baz"

    description = "The foo bar baz command"

    aliases: ClassVar[list[str]] = ["foobarbaz"]

    def handle(self) -> int:
        return 0
