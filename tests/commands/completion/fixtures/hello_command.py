from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar

from cleo.commands.command import Command
from cleo.helpers import option


if TYPE_CHECKING:
    from cleo.io.inputs.option import Option


class HelloCommand(Command):
    name = "hello"
    options: ClassVar[list[Option]] = [
        option(
            "dangerous-option",
            flag=False,
            description="This $hould be `escaped`.",
        ),
        option("option-without-description"),
    ]
    description = "Complete me please."
