from __future__ import annotations

from cleo.commands.command import Command
from cleo.helpers import option
from cleo.io.inputs.argument import Argument


class ListCommand(Command):

    name = "list"

    description = "Lists commands."

    help = """\
The <info>{command_name}</info> command lists all commands:

  <info>{command_full_name}</info>

You can also display the commands for a specific namespace:

  <info>{command_full_name} test</info>
"""

    arguments = [
        Argument("namespace", required=False, description="The namespace name")
    ]
    options = [
        option("version", "V", "Display this application version.", flag=True),
    ]

    def handle(self) -> int:
        if self.option("version"):
            self.io.write_line(self.application.long_version)

            return 0

        from cleo.descriptors.text_descriptor import TextDescriptor

        TextDescriptor().describe(
            self._io, self.application, namespace=self.argument("namespace")
        )

        return 0
