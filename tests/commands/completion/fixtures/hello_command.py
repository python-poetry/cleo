from __future__ import annotations

from cleo.commands.command import Command
from cleo.helpers import option


class HelloCommand(Command):
    name = "hello"
    options = [
        option(
            "dangerous-option",
            flag=False,
            description="This $hould be `escaped`.",
        ),
        option("option-without-description"),
    ]
    description = "Complete me please."
