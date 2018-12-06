from cleo.commands.command import Command


class SignatureCommand(Command):

    name = "no:configure"
    signature = (
        "signature:command {foo : Foo} {bar? : Bar} {--z|baz : Baz} {--Z|bazz : Bazz}"
    )

    description = "description"

    help = "help"

    def handle(self):
        self.line("handle called")
