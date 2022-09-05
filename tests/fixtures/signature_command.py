from __future__ import annotations

from cleo.commands.command import Command
from cleo.helpers import argument
from cleo.helpers import option


class SignatureCommand(Command):
    name = "signature:command"
    options = [
        option("baz", "z", description="Baz"),
        option("bazz", "Z", description="Bazz"),
    ]
    arguments = [
        argument("foo", description="Foo"),
        argument("bar", description="Bar", optional=True),
    ]
    help = "help"
    description = "description"

    def handle(self) -> int:
        self.line("handle called")
        return 0
