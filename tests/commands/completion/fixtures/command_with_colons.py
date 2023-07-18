from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar

from cleo.commands.command import Command
from cleo.helpers import option


if TYPE_CHECKING:
    from cleo.io.inputs.option import Option


class CommandWithColons(Command):
    name = "command:with:colons"
    options: ClassVar[list[Option]] = [option("goodbye")]
    description = "Test."
