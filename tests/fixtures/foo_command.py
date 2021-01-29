from cleo.commands.command import Command
from cleo.io.io import IO


class FooCommand(Command):

    name = "foo bar"

    description = "The foo bar command"

    aliases = ["afoobar"]

    def interact(self, io: IO) -> None:
        io.write_line("interact called")

    def handle(self) -> int:
        self._io.write_line("called")

        return 0
