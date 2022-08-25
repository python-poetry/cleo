from __future__ import annotations

from cleo.commands.command import Command


class Foo3Command(Command):

    name = "foo3"

    description = "The foo3 bar command"

    aliases = ["foo3"]

    def handle(self) -> int:
        question = self.ask("echo:", default="default input")
        self.line(question)
        return 0
