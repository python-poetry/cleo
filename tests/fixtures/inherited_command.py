from __future__ import annotations

from cleo.commands.command import Command


class ParentCommand(Command):
    """
    Parent Command.

    parent
    """


class ChildCommand(ParentCommand):
    pass
