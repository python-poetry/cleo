from __future__ import annotations

from cleo.commands.command import Command
from cleo.helpers import argument
from cleo.helpers import option


class SpacedCommand(Command):
    name = "spaced command"
    description = "Command with space in name."
    arguments = [argument("test", description="test argument")]
    options = [option("goodbye")]
