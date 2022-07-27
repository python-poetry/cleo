from __future__ import annotations

from cleo.commands.command import Command


class SignatureCommand(Command):
    """
    description

    signature:command {foo : Foo} {bar? : Bar} {--z|baz : Baz} {--Z|bazz : Bazz}
    """

    help = "help"

    def handle(self) -> int:
        self.line("handle called")
        return 0
