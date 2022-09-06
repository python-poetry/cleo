from __future__ import annotations

from cleo.commands.command import Command


class ParentCommand(Command):
    name = "parent"
    description = "Parent Command."


class ChildCommand(ParentCommand):
    pass
