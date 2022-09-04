from __future__ import annotations

from cleo.commands.command import Command


class FooSubNamespaced3Command(Command):

    name = "foo bar"

    description = "The foo bar command"

    aliases = ["foobar"]

    def handle(self) -> int:
        question = self.ask("", default="default input")
        self.line(question)
        return 0
