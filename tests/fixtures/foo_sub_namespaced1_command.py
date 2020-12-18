from cleo import Command
from cleo.io.io import IO


class FooSubNamespaced1Command(Command):

    name = "foo bar baz"

    description = "The foo bar baz command"

    aliases = ["foobarbaz"]

    def handle(self) -> int:
        return 0
