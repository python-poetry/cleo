from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar

from cleo.commands.command import Command
from cleo.helpers import argument
from cleo.helpers import option


if TYPE_CHECKING:
    from cleo.io.inputs.argument import Argument
    from cleo.io.inputs.option import Option


class SpacedCommand(Command):
    name = "spaced command"
    description = "Command with space in name."
    arguments: ClassVar[list[Argument]] = [
        argument("test", description="test argument")
    ]
    options: ClassVar[list[Option]] = [option("goodbye")]
