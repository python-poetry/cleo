from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar

from cleo.commands.command import Command
from cleo.helpers import argument
from cleo.helpers import option


if TYPE_CHECKING:
    from cleo.io.inputs.argument import Argument
    from cleo.io.inputs.option import Option


class SignatureCommand(Command):
    name = "signature:command"
    options: ClassVar[list[Option]] = [
        option("baz", "z", description="Baz"),
        option("bazz", "Z", description="Bazz"),
    ]
    arguments: ClassVar[list[Argument]] = [
        argument("foo", description="Foo"),
        argument("bar", description="Bar", optional=True),
    ]
    help = "help"
    description = "description"

    def handle(self) -> int:
        self.line("handle called")
        return 0
