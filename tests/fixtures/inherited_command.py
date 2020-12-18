# -*- coding: utf-8 -*-

from cleo import Command


class ParentCommand(Command):
    """
    Parent Command.

    parent
    """


class ChildCommand(ParentCommand):
    pass
