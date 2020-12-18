from cleo import Command
from cleo.io.io import IO


class Foo2Command(Command):

    name = "foo1 bar"

    description = "The foo1 bar command"

    aliases = ["afoobar2"]

    def handle(self) -> int:
        return 0
