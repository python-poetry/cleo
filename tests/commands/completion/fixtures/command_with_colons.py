from __future__ import annotations

from cleo.commands.command import Command
from cleo.helpers import option


class CommandWithColons(Command):
    name = "command:with:colons"
    options = [option("goodbye", flag=False)]
    description = "Test."
