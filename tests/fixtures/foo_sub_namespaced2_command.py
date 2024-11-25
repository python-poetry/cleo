from __future__ import annotations

from typing import ClassVar

from cleo.commands.command import Command


class FooSubNamespaced2Command(Command):
    name = "foo baz bam"

    description = "The foo baz bam command"

    aliases: ClassVar[list[str]] = ["foobazbam"]

    def handle(self) -> int:
        return 0
