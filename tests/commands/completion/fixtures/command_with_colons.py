from __future__ import annotations

from cleo.commands.command import Command


class CommandWithColons(Command):
    """
    Test.

    command:with:colons
        { --goodbye }
    """
